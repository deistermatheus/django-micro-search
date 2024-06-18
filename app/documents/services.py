from typing import Optional

from pydantic import Field
from openai import OpenAI
from ninja import ModelSchema

from documents.models import Document
from pgvector.django import CosineDistance

EMBEDDING_MODEL = 'text-embedding-3-small'
DIMENSIONS = 512

ai =  OpenAI()


class CreateDocumentDTO(ModelSchema):
    class Meta:
        model = Document
        fields = ['title', 'description']

class GetDocumentDTO(ModelSchema):
    distance: Optional[float] = Field(None)
    class Meta:
        model = Document
        exclude = ['id', 'text_embedding']


class DocumentCommandService():
    @staticmethod
    def create_document(payload: CreateDocumentDTO) -> Document:
        document = Document.objects.create(**payload.dict())

        embeddings = DocumentEmbeddingsService.get_textual_embedding(document)

        document.text_embedding = embeddings
        document.save()

        return document

class DocumentEmbeddingsService():
    @staticmethod
    def get_textual_embedding(document: Document):
        text = f"{document.title} - {document.description}"
        response = ai.embeddings.create(input=text, model=EMBEDDING_MODEL, dimensions=DIMENSIONS)
        return response.data[0].embedding

    @staticmethod
    def get_query_embedding(query):
        response = ai.embeddings.create(input=query, model=EMBEDDING_MODEL, dimensions=DIMENSIONS)
        return response.data[0].embedding

class DocumentQueryService():
    @staticmethod
    def semantic_search(query):
        embedded_query = DocumentEmbeddingsService.get_query_embedding(query)
        documents_with_distance = Document.objects.all().annotate(
            distance=CosineDistance("text_embedding", embedded_query)
        ).order_by("distance")[:3]

        return documents_with_distance