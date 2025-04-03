from ninja import Router, UploadedFile, File

from images.services import (
    CreateImageDocumentDetailsDTO,
    CreateImageResultDTO,
    GetImageDocumentDTO,
    ImageDocumentCommandService,
    ImageDocumentQueryService,
    SearchImageDocumentOptionsDTO,
    SearchImageDocumentsResultDTO,
)

api = Router()


@api.post("/", response=CreateImageResultDTO)
def create_image_document(request, document_data: CreateImageDocumentDetailsDTO, image: UploadedFile = File(None)) -> CreateImageResultDTO:
    return ImageDocumentCommandService.create_image_document(document_data, image)
   


@api.post("/search/", response=SearchImageDocumentsResultDTO)
def query_image_documents(
    request, query_options: SearchImageDocumentOptionsDTO, image: UploadedFile = File(None)
) -> list[GetImageDocumentDTO]:
    return ImageDocumentQueryService.search_image_documents(image, query_options)
