from datetime import datetime
from fastapi import APIRouter, HTTPException
from ..models import ChatRequest, ChatResponse
from ..services.gemini_service import gemini_service
from .. import database

router = APIRouter(prefix="/chat", tags=["Forensic AI Copilot"])

@router.post("", response_model=ChatResponse)
async def chat_copilot_endpoint(payload: ChatRequest):
    """
    Forensic AI Copilot Chat Endpoint:
    Processes natural language queries from investigators regarding case evidence,
    returning analytical findings with exact timestamp references and citations.
    """
    try:
        case_id = payload.case_id
        message = payload.message
        
        # Ingest user question into history
        database.add_chat_message(case_id, "investigator", message, citations=[])
        
        # Retrieve full case knowledge base from SQLite
        case_info = database.get_case_by_id(case_id) or {}
        evidence_items = database.get_evidence_for_case(case_id)
        timeline_events = database.get_timeline_for_case(case_id)
        
        context = {
            "case": case_info,
            "evidence_count": len(evidence_items),
            "evidence_summary": [
                {
                    "type": ev.get("evidence_type"),
                    "filename": ev.get("filename"),
                    "findings": ev.get("analysis_data", {}).get("forensic_summary")
                }
                for ev in evidence_items
            ],
            "timeline": [
                {
                    "time": t.get("timestamp_marker"),
                    "modality": t.get("source_modality"),
                    "event": t.get("description")
                }
                for t in timeline_events
            ]
        }
        
        # Query AI Copilot
        copilot_result = gemini_service.chat_with_copilot(
            case_id=case_id,
            query=message,
            context=context
        )
        
        reply_text = copilot_result.get("reply", "No response generated.")
        citations = copilot_result.get("citations", [])
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Ingest AI reply into chat history
        database.add_chat_message(case_id, "ai_copilot", reply_text, citations=citations)
        
        return {
            "case_id": case_id,
            "reply": reply_text,
            "citations": citations,
            "timestamp": now_str
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Copilot query failed: {str(e)}")

@router.get("/history/{case_id}")
async def get_chat_history_endpoint(case_id: str):
    """Returns persistent chat log for a given case."""
    try:
        return database.get_chat_history(case_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching chat history: {str(e)}")
