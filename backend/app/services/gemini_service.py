import json
import logging
from typing import Dict, Any, Optional
from pathlib import Path
from ..config import settings
from . import mock_service

logger = logging.getLogger(__name__)

class GeminiService:
    def __init__(self):
        self._client = None
        self._init_client()
        
    def _init_client(self):
        if settings.is_gemini_active:
            try:
                from google import genai
                self._client = genai.Client(api_key=settings.GEMINI_API_KEY)
                logger.info("Google Gemini Client initialized successfully.")
            except Exception as e:
                logger.warning(f"Failed to initialize Gemini Client: {e}. Fallback to mock mode.")
                self._client = None
        else:
            self._client = None
            logger.info("Gemini API key not configured or mock mode enabled. Operating with forensic sandbox generators.")

    @property
    def is_available(self) -> bool:
        return self._client is not None

    def analyze_image(self, file_bytes: bytes, mime_type: str, filename: str, case_id: str) -> Dict[str, Any]:
        """Analyzes crime scene image using Gemini Vision or falls back to mock generator."""
        if not self.is_available:
            return mock_service.generate_mock_image_analysis(filename, case_id)
            
        try:
            from google.genai import types
            
            prompt = """
            You are CrimeVision AI, an advanced forensic vision analyst for law enforcement and legal investigation.
            Analyze this crime scene or surveillance image in meticulous forensic detail.
            
            Respond strictly in valid JSON matching this schema:
            {
                "case_id": "<string>",
                "filename": "<string>",
                "person_count": <integer>,
                "persons": [
                    {
                        "id": <integer>,
                        "visual_description": "<string: physical appearance, build, estimated height>",
                        "clothing": "<string: colors, garment types, footwear, masks/gloves>",
                        "stance": "<string: posture, movement, aggression indicators>",
                        "role_inference": "<Suspect|Victim|Security|Witness|Bystander>"
                    }
                ],
                "weapons": [
                    {
                        "weapon_type": "<string: firearm model, blade, blunt object, breaching tool>",
                        "confidence": <float 0.0 to 1.0>,
                        "threat_level": "<LETHAL|HIGH|MEDIUM|LOW>",
                        "location_in_frame": "<string with estimated coordinates or description>",
                        "description": "<string: finish, grip, holster status, magazine extension>"
                    }
                ],
                "evidence_tags": [
                    {
                        "label": "<string: item name>",
                        "category": "<Weapon|Tool|Biological|Impression|Apparel|Electronic>",
                        "confidence": <float 0.0 to 1.0>,
                        "location_in_frame": "<string>",
                        "notes": "<forensic notes on condition, tampering, or significance>"
                    }
                ],
                "scene_environment": {
                    "setting": "<string: indoor vault, corridor, alleyway, street, office>",
                    "lighting": "<string: lux level assessment, shadows, night-vision, camera glare>",
                    "entry_points": ["<list of visible doorways, windows, gates, ducts>"],
                    "exit_points": ["<list of viable egress pathways>"],
                    "security_features_observed": ["<list of cameras, sensors, reinforced doors, locks>"],
                    "environmental_hazards": ["<list of fluids, fire risks, broken glass, obstacles>"]
                },
                "forensic_summary": "<paragraph summarizing the forensic value and crime scene findings>",
                "overall_confidence": <float 0.0 to 1.0>
            }
            """
            
            part = types.Part.from_bytes(data=file_bytes, mime_type=mime_type)
            
            response = self._client.models.generate_content(
                model=settings.GEMINI_MODEL,
                contents=[part, prompt],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.2
                )
            )
            
            data = json.loads(response.text)
            data["case_id"] = case_id
            data["filename"] = filename
            data["is_mock"] = False
            return data
            
        except Exception as e:
            logger.error(f"Gemini image analysis error: {e}. Falling back to sandbox generator.")
            return mock_service.generate_mock_image_analysis(filename, case_id)

    def analyze_audio(self, file_bytes: bytes, mime_type: str, filename: str, case_id: str) -> Dict[str, Any]:
        """Analyzes forensic audio recording using Gemini Audio or falls back to mock generator."""
        if not self.is_available:
            return mock_service.generate_mock_audio_analysis(filename, case_id)
            
        try:
            from google.genai import types
            
            prompt = """
            You are CrimeVision AI Audio Intelligence Engine.
            Transcribe and analyze this forensic audio file (surveillance wire, 911 dispatch, or witness interview).
            Separate speakers carefully into Suspects, Victims, Security/Police, and Witnesses.
            Detect acoustic events (gunshots, door breaches, glass break, vehicle engines).
            Extract key forensic entities (names, locations, mentioned weapons, times).
            
            Respond strictly in valid JSON matching this schema:
            {
                "case_id": "<string>",
                "filename": "<string>",
                "duration_seconds": <float>,
                "transcript_segments": [
                    {
                        "timestamp_start": "<MM:SS.S>",
                        "timestamp_end": "<MM:SS.S>",
                        "speaker_label": "<Suspect 1|Suspect 2|Witness|Night Guard|Officer>",
                        "text": "<exact transcript text>",
                        "tone_emotion": "<string: Urgent|Aggressive|Panicked|Calm>"
                    }
                ],
                "extracted_entities": [
                    {
                        "entity_type": "<PERSON|LOCATION|WEAPON|VEHICLE|TIME|TARGET>",
                        "entity_value": "<string>",
                        "mention_timestamp": "<MM:SS.S>",
                        "context": "<string context explanation>"
                    }
                ],
                "acoustic_events": [
                    {
                        "timestamp": "<MM:SS.S>",
                        "event_type": "<Gunshot|Screaming|Glass Shatter|Engine Roar|Breaching Tool>",
                        "confidence": <float 0.0 to 1.0>,
                        "decibel_profile": "<string estimation, e.g. 95 dB peak>"
                    }
                ],
                "forensic_summary": "<paragraph summarizing the verbal testimony and acoustic findings>",
                "overall_confidence": <float 0.0 to 1.0>
            }
            """
            
            part = types.Part.from_bytes(data=file_bytes, mime_type=mime_type)
            
            response = self._client.models.generate_content(
                model=settings.GEMINI_MODEL,
                contents=[part, prompt],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.2
                )
            )
            
            data = json.loads(response.text)
            data["case_id"] = case_id
            data["filename"] = filename
            data["is_mock"] = False
            return data
            
        except Exception as e:
            logger.error(f"Gemini audio analysis error: {e}. Falling back to sandbox generator.")
            return mock_service.generate_mock_audio_analysis(filename, case_id)

    def analyze_video(self, file_bytes: bytes, mime_type: str, filename: str, case_id: str) -> Dict[str, Any]:
        """Analyzes surveillance video using Gemini Video or falls back to mock generator."""
        if not self.is_available:
            return mock_service.generate_mock_video_analysis(filename, case_id)
            
        try:
            from google.genai import types
            
            prompt = """
            You are CrimeVision AI Video Telemetry Engine.
            Analyze this surveillance video file frame-by-frame.
            Identify key actions, perimeter breaches, weapon movements, and suspect egress.
            Generate a temporal event log with high-precision timestamp markers.
            
            Respond strictly in valid JSON matching this schema:
            {
                "case_id": "<string>",
                "filename": "<string>",
                "duration_seconds": <float>,
                "keyframe_events": [
                    {
                        "timestamp": "<MM:SS.S>",
                        "action_detected": "<string: concise description of action>",
                        "subject_description": "<string: who performed the action>",
                        "scene_location": "<string: area within camera view>",
                        "confidence": <float 0.0 to 1.0>,
                        "severity": "<CRITICAL|HIGH|MEDIUM|LOW>"
                    }
                ],
                "temporal_summary": "<summary of chronological developments observed>",
                "detected_actions_count": <integer>,
                "overall_confidence": <float 0.0 to 1.0>
            }
            """
            
            part = types.Part.from_bytes(data=file_bytes, mime_type=mime_type)
            
            response = self._client.models.generate_content(
                model=settings.GEMINI_MODEL,
                contents=[part, prompt],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.2
                )
            )
            
            data = json.loads(response.text)
            data["case_id"] = case_id
            data["filename"] = filename
            data["is_mock"] = False
            mock_service.ensure_synthetic_keyframes()
            return data
            
        except Exception as e:
            logger.error(f"Gemini video analysis error: {e}. Falling back to sandbox generator.")
            return mock_service.generate_mock_video_analysis(filename, case_id)

    def chat_with_copilot(self, case_id: str, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Conversational forensic copilot querying fused case evidence with citations."""
        if not self.is_available:
            return mock_service.generate_mock_chat_response(case_id, query, context)
            
        try:
            from google.genai import types
            
            context_str = json.dumps(context, indent=2)
            prompt = f"""
            You are CrimeVision AI Forensic Copilot, an elite AI forensic investigator.
            You assist lead detectives, prosecutors, and forensic specialists by answering inquiries
            regarding Case '{case_id}'.
            
            CASE CONTEXT AND FUSED EVIDENCE:
            {context_str}
            
            INVESTIGATOR QUERY:
            "{query}"
            
            INSTRUCTIONS:
            1. Formulate a comprehensive, analytical forensic answer grounded in the evidence provided.
            2. Cross-reference across modalities (Images, Audio transcripts, Video temporal logs).
            3. Highlight suspect contradictions or alibi discrepancies if relevant.
            4. Provide specific timestamp and source citations.
            
            Respond strictly in valid JSON matching this schema:
            {{
                "case_id": "{case_id}",
                "reply": "<detailed markdown response with bold headers, bullet points, and citations in text>",
                "citations": [
                    {{
                        "source": "<e.g. CAM-01 IMAGE / SENSOR-02 AUDIO>",
                        "timestamp": "<timestamp marker or MM:SS>",
                        "details": "<short quote or detection note>"
                    }}
                ],
                "timestamp": "<current timestamp>"
            }}
            """
            
            response = self._client.models.generate_content(
                model=settings.GEMINI_MODEL,
                contents=[prompt],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.3
                )
            )
            
            return json.loads(response.text)
            
        except Exception as e:
            logger.error(f"Gemini chat error: {e}. Falling back to sandbox generator.")
            return mock_service.generate_mock_chat_response(case_id, query, context)

gemini_service = GeminiService()
