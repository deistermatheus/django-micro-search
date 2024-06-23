from ninja import NinjaAPI
from typing import Dict
from documents.api import api as documents_api
from images.api import api as images_api

api = NinjaAPI(
    title="Indexing and Retrieval with AI", description="Demo API for Hybrid and Multimodal search using Django Ninja"
)


@api.get("/health/", tags=["root"])
def health(request) -> Dict[str, bool]:
    return {"ok": True}


api.add_router("/documents/", documents_api, tags=["documents"])
api.add_router("/image-documents", images_api, tags=["images"])
