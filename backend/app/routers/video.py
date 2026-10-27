import os
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from ..config import settings
from .. import database
from ..models import VideoAnalysisResponse
from ..services.gemini_service import gemini_service

router = APIRouter(prefix="/analyze", tags=["Video Analysis"])

@router.post("/video", response_model=VideoAnalysisResponse)
async def analyze_video_endpoint(
    file: UploadFile = File(...),
    case_id: str = Form("CASE-2026-0891")
):
    """
    Multimodal Video Analysis Endpoint:
    Processes surveillance footage (.mp4, .avi).
    Performs temporal action breakdown and generates timestamped event logs.
    """
    try:
        file_bytes = await file.read()
        file_size = len(file_bytes)
        
        safe_filename = f"vid_{case_id}_{file.filename}"
        dest_path = settings.UPLOAD_DIR / safe_filename
        with open(dest_path, "wb") as f:
            f.write(file_bytes)
            
        mime_type = file.content_type or "video/mp4"
        
        # Analyze using Gemini Video or fallback mock
        analysis_data = gemini_service.analyze_video(
            file_bytes=file_bytes,
            mime_type=mime_type,
            filename=file.filename,
            case_id=case_id
        )
        analysis_data["file_url"] = f"/uploads/{safe_filename}"
        
        # Ingest into SQLite evidence table
        evidence_id = database.add_evidence(
            case_id=case_id,
            evidence_type="VIDEO",
            filename=file.filename,
            file_path=str(dest_path),
            file_size=file_size,
            mime_type=mime_type,
            analysis_json=analysis_data
        )
        
        # Ingest temporal keyframe actions into timeline
        for kf in analysis_data.get("keyframe_events", []):
            database.add_timeline_event(
                case_id=case_id,
                timestamp_marker=f"+{kf.get('timestamp')}",
                source_modality="VIDEO",
                event_type="SURVEILLANCE_ACTION",
                description=f"{kf.get('action_detected')} [{kf.get('scene_location')}]. {kf.get('subject_description')}",
                confidence=kf.get("confidence", 0.95),
                entities_involved=kf.get("subject_description", ""),
                severity=kf.get("severity", "HIGH")
            )
            
        return analysis_data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Video analysis error: {str(e)}")
