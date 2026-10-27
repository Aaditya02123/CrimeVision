from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

# --- Case Models ---
class CaseCreate(BaseModel):
    case_id: str = Field(..., description="Unique case identifier, e.g. CASE-2026-0999")
    title: str = Field(..., description="Case title")
    incident_type: str = Field(..., description="Category, e.g. Robbery, Burglary, Assault")
    location: str = Field(..., description="Crime scene location")
    incident_date: Optional[str] = Field(None, description="Date and time of incident")
    investigator: Optional[str] = Field("Lead Investigator", description="Investigator in charge")
    status: Optional[str] = Field("ACTIVE", description="ACTIVE, UNDER_REVIEW, SOLVED, ARCHIVED")
    severity: Optional[str] = Field("HIGH", description="CRITICAL, HIGH, MEDIUM, LOW")
    summary: Optional[str] = Field("", description="Executive summary of the case")

class CaseResponse(BaseModel):
    case_id: str
    title: str
    incident_type: str
    location: str
    incident_date: str
    investigator: str
    status: str
    severity: str
    summary: Optional[str] = None
    created_at: str

# --- Image Analysis Models ---
class PersonDetail(BaseModel):
    id: int
    visual_description: str
    clothing: str
    stance: str
    role_inference: str  # Suspect, Victim, Bystander, Security

class WeaponDetail(BaseModel):
    weapon_type: str
    confidence: float
    threat_level: str  # LETHAL, HIGH, MEDIUM
    location_in_frame: str
    description: str

class EvidenceTag(BaseModel):
    label: str
    category: str  # Weapon, Tool, Biological, Apparel, Footwear
    confidence: float
    location_in_frame: str
    notes: str

class SceneEnvironment(BaseModel):
    setting: str
    lighting: str
    entry_points: List[str]
    exit_points: List[str]
    security_features_observed: List[str]
    environmental_hazards: List[str]

class ImageAnalysisResponse(BaseModel):
    case_id: str
    filename: str
    person_count: int
    persons: List[PersonDetail]
    weapons: List[WeaponDetail]
    evidence_tags: List[EvidenceTag]
    scene_environment: SceneEnvironment
    forensic_summary: str
    overall_confidence: float
    is_mock: bool = False
    file_url: Optional[str] = None

# --- Audio Analysis Models ---
class AudioSegment(BaseModel):
    timestamp_start: str
    timestamp_end: str
    speaker_label: str  # Suspect 1, Suspect 2, Witness, Victim, Dispatcher
    text: str
    tone_emotion: str

class ForensicEntity(BaseModel):
    entity_type: str  # PERSON, LOCATION, WEAPON, TIME, VEHICLE
    entity_value: str
    mention_timestamp: str
    context: str

class AcousticEvent(BaseModel):
    timestamp: str
    event_type: str  # Gunshot, Screaming, Glass Shatter, Footsteps, Vehicle Engine
    confidence: float
    decibel_profile: Optional[str] = "High Impulse"

class AudioAnalysisResponse(BaseModel):
    case_id: str
    filename: str
    duration_seconds: float
    transcript_segments: List[AudioSegment]
    extracted_entities: List[ForensicEntity]
    acoustic_events: List[AcousticEvent]
    forensic_summary: str
    overall_confidence: float
    is_mock: bool = False
    file_url: Optional[str] = None

# --- Video Analysis Models ---
class VideoKeyframeEvent(BaseModel):
    timestamp: str
    action_detected: str
    subject_description: str
    scene_location: str
    confidence: float
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW
    keyframe_preview_path: Optional[str] = None

class VideoAnalysisResponse(BaseModel):
    case_id: str
    filename: str
    duration_seconds: float
    keyframe_events: List[VideoKeyframeEvent]
    temporal_summary: str
    detected_actions_count: int
    overall_confidence: float
    is_mock: bool = False
    file_url: Optional[str] = None

# --- Fusion & Intelligence Models ---
class TimelineEventItem(BaseModel):
    id: Optional[int] = None
    case_id: str
    timestamp_marker: str
    source_modality: str  # IMAGE, AUDIO, VIDEO, FUSED
    event_type: str
    description: str
    confidence: float
    entities_involved: Optional[str] = ""
    severity: str  # CRITICAL, HIGH, MEDIUM, INFO

class CrimeClassification(BaseModel):
    primary_offense: str
    secondary_tags: List[str]
    confidence: float
    severity: str
    justification: str
    legal_statutes: List[str]

class TimelineFusionResponse(BaseModel):
    case_id: str
    timeline: List[TimelineEventItem]
    classification: CrimeClassification
    contradictions_detected: List[str]
    fusion_summary: str

# --- Chat Models ---
class Citation(BaseModel):
    source: str
    timestamp: Optional[str] = None
    details: str

class ChatRequest(BaseModel):
    case_id: str
    message: str

class ChatResponse(BaseModel):
    case_id: str
    reply: str
    citations: List[Citation]
    timestamp: str

# --- Report Models ---
class ReportGenerateRequest(BaseModel):
    case_id: str
    include_images: bool = True
    include_audio: bool = True
    include_video: bool = True
    include_timeline: bool = True
    include_classification: bool = True
    include_chat_summary: bool = True
    investigator_notes: Optional[str] = ""

class ReportGenerateResponse(BaseModel):
    case_id: str
    filename: str
    pdf_url: str
    generated_at: str
    file_size_bytes: int
