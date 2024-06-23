from ninja import Router
from ninja.errors import HttpError
from typing import List

from documents.services import (
    CreateDocumentDTO,
    GetDocumentDTO,
    DocumentCommandService,
    DocumentQueryService,
    SearchChoices,
)

api = Router()


@api.post("/", response=GetDocumentDTO)
def create_document(request, payload: CreateDocumentDTO):
    """
    Creates text based documents with title and description:
    """
    return DocumentCommandService.create_document(payload)


@api.get("/search/", response=List[GetDocumentDTO])
def query_documents(request, q: str, mode: SearchChoices = "semantic"):
    """
    Retrieves text based on query and search choice provided. Defaults to
    semantic search:
    """
    mapper = {
        "semantic": DocumentQueryService.semantic_search,
        "textual": DocumentQueryService.text_search,
        "hybrid": DocumentQueryService.hybrid_search,
    }

    query_handler = mapper.get(mode, None)

    if query_handler:
        return query_handler(q)

    raise HttpError(400, "Bad Request")
