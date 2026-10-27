from fastapi import APIRouter, HTTPException
from ..services.fusion_engine import fuse_case_evidence
from ..models import TimelineFusionResponse, CrimeClassification
from .. import database

router = APIRouter(prefix="/fusion", tags=["Multimodal Fusion & Intelligence"])

@router.get("/timeline/{case_id}", response_model=TimelineFusionResponse)
@router.post("/fuse/{case_id}", response_model=TimelineFusionResponse)
async def get_fused_timeline_endpoint(case_id: str):
    """
    Multimodal Fusion Endpoint:
    Blends image detections, audio transcript segments, and video keyframes
    into an unified chronological timeline with automated crime classification.
    """
    try:
        fusion_result = fuse_case_evidence(case_id)
        return fusion_result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fusion error: {str(e)}")

@router.get("/classify/{case_id}", response_model=CrimeClassification)
async def get_classification_endpoint(case_id: str):
    """
    Automated Crime Classifier Endpoint:
    Assesses all multimodal markers and produces primary offense, legal statutes, and severity.
    """
    try:
        fusion_result = fuse_case_evidence(case_id)
        return fusion_result["classification"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Classification error: {str(e)}")
