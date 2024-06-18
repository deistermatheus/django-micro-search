from typing import Optional, List
from collections import defaultdict
from enum import Enum

from pydantic import Field
from openai import OpenAI
from ninja import ModelSchema

from documents.models import Document
from pgvector.django import CosineDistance

from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector

EMBEDDING_MODEL = 'text-embedding-3-small'
DIMENSIONS = 512

ai =  OpenAI()


class CreateDocumentDTO(ModelSchema):
    class Meta:
        model = Document
        fields = ['title', 'description']

class GetDocumentDTO(ModelSchema):
    distance: Optional[float] = Field(None)
    rank: Optional[float] = Field(None)
    class Meta:
        model = Document
        exclude = ['id', 'text_embedding']

class SearchChoices(str, Enum):
    semantic = 'semantic'
    textual = 'textual'
    hybrid = 'hybrid'

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

    @staticmethod
    def text_search(query):
        vector = SearchVector("title", "description")
        parsed_query = SearchQuery(query)
        documents_with_rank = Document.objects.all().annotate(
            rank=SearchRank(vector, parsed_query)
        ).order_by("-rank")[:3]

        return documents_with_rank

    @staticmethod
    def hybrid_search(query):
        text_result = list(DocumentQueryService.text_search(query))
        semantic_result = list(DocumentQueryService.semantic_search(query))

        combined_result = DocumentQueryService.reciprocal_rank_fusion(text_result, semantic_result)[:3]

        return combined_result


    @staticmethod
    def reciprocal_rank_fusion(list1: List[Document], list2: List[Document], k: int = 60) -> List[Document]:
        def score(rank: int) -> float:
            return 1.0 / (rank + k)

        scores = defaultdict(float)

        for rank, doc in enumerate(list1):
            scores[doc.uuid] += score(rank)

        for rank, doc in enumerate(list2):
            scores[doc.uuid] += score(rank)

        combined_scores = [(doc, scores[doc.uuid]) for doc in set(list1 + list2)]

        combined_scores.sort(key=lambda x: x[1], reverse=True)


        combined_ranked_list = [doc for doc, _ in combined_scores]

        return combined_ranked_list
