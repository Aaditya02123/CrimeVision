import os
from datetime import datetime
from pathlib import Path
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from ..config import settings
from ..models import ReportGenerateRequest, ReportGenerateResponse
from ..services.pdf_generator import generate_case_pdf_report

router = APIRouter(prefix="/report", tags=["Forensic Report Exporter"])

@router.post("/generate", response_model=ReportGenerateResponse)
async def generate_report_endpoint(payload: ReportGenerateRequest):
    """
    Forensic Report Generator:
    Compiles full multimodal evidence findings, audio transcripts,
    surveillance timelines, and chain-of-custody verification into a downloadable PDF.
    """
    try:
        case_id = payload.case_id
        options = payload.model_dump()
        
        pdf_file_path = generate_case_pdf_report(case_id, options)
        p = Path(pdf_file_path)
        file_size = p.stat().st_size
        filename = p.name
        
        return {
            "case_id": case_id,
            "filename": filename,
            "pdf_url": f"/api/v1/report/download/{case_id}",
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "file_size_bytes": file_size
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {str(e)}")

@router.get("/download/{case_id}")
async def download_report_endpoint(case_id: str):
    """Downloads the latest generated forensic PDF report for a case."""
    try:
        # Check matching report files in report directory
        candidates = sorted(settings.REPORT_DIR.glob(f"CRIMEVISION_{case_id}_*.pdf"), key=os.path.getmtime, reverse=True)
        if not candidates:
            # Generate one on the fly if not found
            pdf_path = generate_case_pdf_report(case_id)
        else:
            pdf_path = str(candidates[0])
            
        return FileResponse(
            path=pdf_path,
            filename=Path(pdf_path).name,
            media_type="application/pdf"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Download failed: {str(e)}")

@router.get("/file/{filename}")
async def download_named_file_endpoint(filename: str):
    """Downloads a specific generated PDF report by filename."""
    pdf_path = settings.REPORT_DIR / filename
    if not pdf_path.exists():
        raise HTTPException(status_code=404, detail="Report file not found")
        
    return FileResponse(
        path=str(pdf_path),
        filename=filename,
        media_type="application/pdf"
    )
