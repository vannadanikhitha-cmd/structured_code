from fastapi import APIRouter

from app.schemas.pdf_request import PDFRequest
from app.services.pdf_extraction_service import (extract_table_from_pdf)

router = APIRouter()


@router.post("/extract-table")
async def pdf_to_csv(request: PDFRequest):
    return await extract_table_from_pdf(request)