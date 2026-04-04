from fastapi import APIRouter, UploadFile, File, Form

from app.services.pdf_loader import load_pdf_pages
from app.graph.workflow import build_graph

router = APIRouter()
graph = build_graph()

@router.post("/process")
async def process_claim(
    claim_id: str = Form(...),
    file: UploadFile = File(...)
):
    pages = load_pdf_pages(file.file)

    result = graph.invoke({
        "claim_id": claim_id,
        "pages": pages
    })

    return result["final_output"]