from typing import List, Dict, Any
from fastapi import APIRouter, HTTPException
from ..models import CaseCreate, CaseResponse
from .. import database

router = APIRouter(prefix="/cases", tags=["Case Management"])

@router.get("", response_model=List[Dict[str, Any]])
async def list_cases():
    """List all registered forensic cases."""
    return database.get_cases()

@router.post("", response_model=Dict[str, Any])
async def create_new_case(payload: CaseCreate):
    """Register a new criminal case in the forensic database."""
    existing = database.get_case_by_id(payload.case_id)
    if existing:
        raise HTTPException(status_code=400, detail="A case with this Case ID already exists.")
    created = database.create_case(payload.model_dump())
    return created

@router.get("/{case_id}")
async def get_case_detail(case_id: str):
    """Retrieve metadata for a specific case."""
    case = database.get_case_by_id(case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return case

@router.get("/{case_id}/stats")
async def get_case_stats(case_id: str):
    """Retrieve statistical metrics and evidence counts for a case."""
    return database.get_case_statistics(case_id)

@router.get("/{case_id}/evidence")
async def get_case_evidence(case_id: str):
    """Retrieve all ingested multimodal evidence items for a case."""
    return database.get_evidence_for_case(case_id)

@router.get("/{case_id}/timeline")
async def get_case_timeline(case_id: str):
    """Retrieve chronological timeline markers for a case."""
    return database.get_timeline_for_case(case_id)
