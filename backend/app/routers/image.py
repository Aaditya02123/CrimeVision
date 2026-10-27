import os
import shutil
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from ..config import settings
from .. import database
from ..models import ImageAnalysisResponse
from ..services.gemini_service import gemini_service

router = APIRouter(prefix="/analyze", tags=["Image Analysis"])

@router.post("/image", response_model=ImageAnalysisResponse)
async def analyze_image_endpoint(
    file: UploadFile = File(...),
    case_id: str = Form("CASE-2026-0891")
):
    """
    Multimodal Image Analysis Endpoint:
    Accepts forensic crime scene photographs or CCTV frames.
    Extracts person counts, weapon identifications, evidence tags, and entry/exit environment.
    """
    try:
        file_bytes = await file.read()
        file_size = len(file_bytes)
        
        # Save file to uploads directory
        safe_filename = f"img_{case_id}_{file.filename}"
        dest_path = settings.UPLOAD_DIR / safe_filename
        with open(dest_path, "wb") as f:
            f.write(file_bytes)
            
        mime_type = file.content_type or "image/jpeg"
        
        # Analyze using Gemini Vision or fallback mock
        analysis_data = gemini_service.analyze_image(
            file_bytes=file_bytes,
            mime_type=mime_type,
            filename=file.filename,
            case_id=case_id
        )
        analysis_data["file_url"] = f"/uploads/{safe_filename}"
        
        # Ingest into SQLite evidence table
        evidence_id = database.add_evidence(
            case_id=case_id,
            evidence_type="IMAGE",
            filename=file.filename,
            file_path=str(dest_path),
            file_size=file_size,
            mime_type=mime_type,
            analysis_json=analysis_data
        )
        
        # Automatically register critical weapon events in timeline
        weapons = analysis_data.get("weapons", [])
        for w in weapons:
            if w.get("threat_level") in ("LETHAL", "HIGH"):
                database.add_timeline_event(
                    case_id=case_id,
                    timestamp_marker="23:41:15",
                    source_modality="IMAGE",
                    event_type="WEAPON_DETECTED",
                    description=f"{w.get('weapon_type')} detected: {w.get('description', '')}",
                    confidence=w.get("confidence", 0.95),
                    entities_involved=w.get("weapon_type"),
                    severity="CRITICAL" if w.get("threat_level") == "LETHAL" else "HIGH"
                )
                
        return analysis_data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image analysis error: {str(e)}")
