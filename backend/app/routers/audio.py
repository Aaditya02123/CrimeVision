import os
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from ..config import settings
from .. import database
from ..models import AudioAnalysisResponse
from ..services.gemini_service import gemini_service

router = APIRouter(prefix="/analyze", tags=["Audio Analysis"])

@router.post("/audio", response_model=AudioAnalysisResponse)
async def analyze_audio_endpoint(
    file: UploadFile = File(...),
    case_id: str = Form("CASE-2026-0891")
):
    """
    Multimodal Audio Analysis Endpoint:
    Processes dispatch recordings, wiretaps, or witness interviews (.wav, .mp3, .m4a).
    Generates speaker-attributed transcripts, extracts named entities, and tags acoustic events.
    """
    try:
        file_bytes = await file.read()
        file_size = len(file_bytes)
        
        safe_filename = f"aud_{case_id}_{file.filename}"
        dest_path = settings.UPLOAD_DIR / safe_filename
        with open(dest_path, "wb") as f:
            f.write(file_bytes)
            
        mime_type = file.content_type or "audio/wav"
        
        # Analyze using Gemini Audio or fallback mock
        analysis_data = gemini_service.analyze_audio(
            file_bytes=file_bytes,
            mime_type=mime_type,
            filename=file.filename,
            case_id=case_id
        )
        analysis_data["file_url"] = f"/uploads/{safe_filename}"
        
        # Ingest into SQLite evidence table
        evidence_id = database.add_evidence(
            case_id=case_id,
            evidence_type="AUDIO",
            filename=file.filename,
            file_path=str(dest_path),
            file_size=file_size,
            mime_type=mime_type,
            analysis_json=analysis_data
        )
        
        # Ingest acoustic events and high-stress utterances into timeline
        for ac in analysis_data.get("acoustic_events", []):
            database.add_timeline_event(
                case_id=case_id,
                timestamp_marker=f"+{ac.get('timestamp')}",
                source_modality="AUDIO",
                event_type="ACOUSTIC_EVENT",
                description=f"Audio signature detected: {ac.get('event_type')} ({ac.get('decibel_profile')})",
                confidence=ac.get("confidence", 0.92),
                entities_involved="Acoustic Sensor",
                severity="CRITICAL" if "shot" in ac.get("event_type", "").lower() else "HIGH"
            )
            
        return analysis_data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Audio analysis error: {str(e)}")
