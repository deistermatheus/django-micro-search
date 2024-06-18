from ninja import NinjaAPI
from typing import Dict, List

from documents.services import CreateDocumentDTO, GetDocumentDTO,  DocumentCommandService, DocumentQueryService

api = NinjaAPI()

@api.get("/health")
def health(request)-> Dict[str, bool]:
    return {"ok": True}

@api.post("/documents", response=GetDocumentDTO)
def create_document(request, payload: CreateDocumentDTO):
    return DocumentCommandService.create_document(payload)


@api.get("/documents", response=List[GetDocumentDTO])
def query_documents(request, q):
    return DocumentQueryService.semantic_search(q)
