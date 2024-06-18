from ninja import NinjaAPI
from ninja.errors import HttpError
from typing import Dict, List

from documents.services import CreateDocumentDTO, GetDocumentDTO,  DocumentCommandService, DocumentQueryService, SearchChoices

api = NinjaAPI()

@api.get("/health")
def health(request)-> Dict[str, bool]:
    return {"ok": True}

@api.post("/documents/", response=GetDocumentDTO)
def create_document(request, payload: CreateDocumentDTO):
    return DocumentCommandService.create_document(payload)


@api.get("/documents/search", response=List[GetDocumentDTO])
def query_documents(request, q: str, mode: SearchChoices = 'semantic'):
    mapper = {
        'semantic':  DocumentQueryService.semantic_search,
        'textual': DocumentQueryService.text_search
    }

    query_handler = mapper.get(mode, None)

    if query_handler:
        return query_handler(q)

    raise HttpError(400, "Bad Request")
