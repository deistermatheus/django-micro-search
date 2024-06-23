from ninja import Router, UploadedFile, File

from images.services import (
    CreateImageDocumentDetailsDTO,
    GetImageDocumentDTO,
    ImageDocumentCommandService,
    ImageDocumentQueryService,
    SearchImageDocumentOptionsDTO,
)

api = Router()


@api.post("/")
def create_image_document(request, document_data: CreateImageDocumentDetailsDTO, image: UploadedFile = File(None)):
    return ImageDocumentCommandService.create_image_document(document_data, image)


@api.post("/search/")
def query_image_documents(
    request, query_options: SearchImageDocumentOptionsDTO, image: UploadedFile = File(None)
) -> list[GetImageDocumentDTO]:
    return ImageDocumentQueryService.search_image_documents(image, query_options)
