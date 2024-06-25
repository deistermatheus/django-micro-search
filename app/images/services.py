import requests
from typing import List
from django.core.files.storage import default_storage
from ninja import ModelSchema, Schema
from ninja.files import UploadedFile
from images.models import ImageDocument
from typing import Optional
from pydantic import Field
from openai import OpenAI
from pgvector.django import CosineDistance
from images.ml_models import clip as CLIPModel
import base64
from io import BytesIO
from PIL import Image


ai = OpenAI()


class CreateImageDocumentDetailsDTO(Schema):
    title: str
    description: str


class SearchImageDocumentOptionsDTO(Schema):
    analyze_results: bool = False
    user_prompt: str = """
    Compare the uploaded image with the provided images and give a reasoning of why they might be similar.
    They were the top N in a similarity search
    """


class GetImageDocumentDTO(ModelSchema):
    distance: Optional[float] = Field(None)

    @staticmethod
    def from_orm(instance):
        instance_dict = {
            "id": instance.id,
            "title": instance.title,
            "description": instance.description,
            "created_at": instance.created_at,
            "image": instance.image.url if instance.image else None,
            "distance": instance.distance,
        }
        return GetImageDocumentDTO(**instance_dict)

    class Meta:
        model = ImageDocument
        exclude = ["id", "image_embedding"]

class CreateImageResultDTO(CreateImageDocumentDetailsDTO):
    image: str


class SearchImageDocumentsResultDTO(Schema):
    similar: List[GetImageDocumentDTO]
    reasoning: Optional[str] = Field(None)


class ImageDocumentCommandService:
    @staticmethod
    def create_image_document(details: CreateImageDocumentDetailsDTO, image: UploadedFile)-> CreateImageResultDTO:
        image_name = default_storage.save(image.name, image)

        details_dict = details.dict()
        image_embedding = CLIPModel.embed_image(image.file)
        document = ImageDocument.objects.create(**details_dict, image_embedding=image_embedding, image=image_name)

        return {**details_dict, "image": document.image.url}


class ImageDocumentQueryService:
    @staticmethod
    def convert_local_image_to_base64(buffer):
        return base64.b64encode(buffer.getvalue()).decode("utf-8")

    @staticmethod
    def convert_remote_image_to_base64(image_url):
        try:
            response = requests.get(image_url)
            response.raise_for_status()  # Raise an exception for HTTP errors

            image = Image.open(BytesIO(response.content))
            buffer = BytesIO()
            if image.mode == "RGBA":
                image = image.convert("RGB")
            image.save(buffer, format="JPEG")
            image_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

            return image_base64

        except requests.exceptions.RequestException as e:
            print(f"Error fetching image from URL: {e}")
            return None

    @staticmethod
    def get_ai_analysis(documents_with_distance, image, user_prompt):
        base64_images = [
            ImageDocumentQueryService.convert_remote_image_to_base64(image.image.url)
            for image in documents_with_distance
        ]

        uploaded_image_base64 = ImageDocumentQueryService.convert_local_image_to_base64(image.file)

        messages = [
            {"role": "system", "content": user_prompt},
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpg;base64,{uploaded_image_base64}", "detail": "low"},
                    },
                    *[
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpg;base64,{img_base64}", "detail": "low"},
                        }
                        for img_base64 in base64_images
                    ],
                ],
            },
        ]

        response = ai.chat.completions.create(
            messages=messages,
            model="gpt-4o",
            temperature=0,
        )

        reasoning = response.choices[0].message.content

        return reasoning

    @staticmethod
    def search_image_documents(
        image: UploadedFile, query_options: SearchImageDocumentOptionsDTO
    ) -> SearchImageDocumentsResultDTO:
        image_embedding = CLIPModel.embed_image(image.file)

        documents_with_distance = (
            ImageDocument.objects.all()
            .annotate(distance=CosineDistance("image_embedding", image_embedding))
            .order_by("distance")[:3]
        )

        results = {"similar": [GetImageDocumentDTO.from_orm(doc) for doc in documents_with_distance]}

        if query_options.analyze_results:
            reasoning = ImageDocumentQueryService.get_ai_analysis(
                documents_with_distance, image, query_options.user_prompt
            )
            results["reasoning"] = reasoning

        return results
