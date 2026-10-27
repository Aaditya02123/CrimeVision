import os
from typing import Dict, Any, List
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from ..config import settings

def generate_mock_image_analysis(filename: str, case_id: str) -> Dict[str, Any]:
    """Generates realistic multimodal forensic image analysis fallback data."""
    fn_lower = filename.lower()
    
    if "alley" in fn_lower or "escape" in fn_lower or "outdoor" in fn_lower:
        return {
            "case_id": case_id,
            "filename": filename,
            "person_count": 2,
            "persons": [
                {
                    "id": 1,
                    "visual_description": "Male adult, approx 5'11'', athletic build, wearing dark tactical balaclava",
                    "clothing": "Matte black windbreaker, charcoal cargo trousers, combat-grade boots with reinforced soles",
                    "stance": "Rapid locomotion, torso angled forward at 45 degrees, carrying heavy duffle in left hand",
                    "role_inference": "Suspect (Perpetrator 1)"
                },
                {
                    "id": 2,
                    "visual_description": "Individual approx 5'9'', wearing high-visibility security windbreaker with ripped shoulder",
                    "clothing": "Navy municipal security uniform, reflective silver chevron striping",
                    "stance": "Recumbent position on concrete surface, protective posture guarding cranium",
                    "role_inference": "Victim / Security Guard"
                }
            ],
            "weapons": [
                {
                    "weapon_type": "Glock 19 Semi-Automatic 9mm Handgun",
                    "confidence": 0.96,
                    "threat_level": "LETHAL",
                    "location_in_frame": "Holstered on right tactical thigh rig (Bounding Box: [640, 720, 710, 810])",
                    "description": "Polymer frame firearm with extended 24-round magazine visible"
                },
                {
                    "weapon_type": "Blunt Force Tactical Crowbar / Pry Tool",
                    "confidence": 0.91,
                    "threat_level": "HIGH",
                    "location_in_frame": "Discarded on alley pavement near drainage grate",
                    "description": "36-inch hardened forged carbon-steel pry bar with blue rubber grip"
                }
            ],
            "evidence_tags": [
                {
                    "label": "Thermal Cutting Torch Residue",
                    "category": "Tool",
                    "confidence": 0.94,
                    "location_in_frame": "Discolored scorch ring on external metallic service portal",
                    "notes": "Slag pattern indicates exothermic reaction consistent with magnesium lance"
                },
                {
                    "label": "Tire Tread Impression",
                    "category": "Impression",
                    "confidence": 0.88,
                    "location_in_frame": "Asphalt perimeter curb edge",
                    "notes": "Directional tread matches high-performance all-weather commercial radial tires"
                },
                {
                    "label": "Latent Blood Transfer Smear",
                    "category": "Biological",
                    "confidence": 0.92,
                    "location_in_frame": "Vertical brick column at 1.4m height",
                    "notes": "Contact transfer smear; probable source: suspect left forearm laceration"
                }
            ],
            "scene_environment": {
                "setting": "Industrial back alleyway adjacent to rear vault loading dock",
                "lighting": "Low ambient sodium vapor lighting (approx 4.2 lux) supplemented by camera infrared emitter",
                "entry_points": ["Sub-level freight elevator doorway", "Unsecured fire egress stairwell #3"],
                "exit_points": ["North alleyway opening onto 5th Avenue commercial thoroughfare"],
                "security_features_observed": ["CCTV Dome Camera (disabled via spray)", "Magnetic reed switch contact broken"],
                "environmental_hazards": ["Wet concrete slickness", "High-voltage conduit exposed near transformer"]
            },
            "forensic_summary": "Surveillance snapshot captures active egress of primary armed suspect following security guard neutralization. Lethal sidearm and industrial forced-entry implements positively identified with 96% forensic certainty.",
            "overall_confidence": 0.95,
            "is_mock": True
        }
    else:
        # Default Vault / Interior Scene
        return {
            "case_id": case_id,
            "filename": filename,
            "person_count": 2,
            "persons": [
                {
                    "id": 1,
                    "visual_description": "Perpetrator Alpha: Height 182cm, tactical mask, Kevlar level III vest",
                    "clothing": "All-black Nomex tactical jumpsuit, carbon-fiber knuckle gloves, balaclava",
                    "stance": "Standing at vault perimeter, weapon drawn in Weaver ready stance",
                    "role_inference": "Primary Armed Suspect"
                },
                {
                    "id": 2,
                    "visual_description": "Perpetrator Beta: Height 175cm, mechanical backpack apparatus",
                    "clothing": "Dark grey tactical coveralls, heavy leather welding gloves, protective eye goggles",
                    "stance": "Kneeling before vault mechanical locking spindle, operating pneumatic breach gear",
                    "role_inference": "Technical Breach Accomplice"
                }
            ],
            "weapons": [
                {
                    "weapon_type": "Sig Sauer P320 9mm Handgun",
                    "confidence": 0.97,
                    "threat_level": "LETHAL",
                    "location_in_frame": "Drawn in suspect right hand, aimed toward entrance hallway [BBox: [450, 600, 520, 680]]",
                    "description": "Tactical sidearm with mounted flashlight attachment"
                },
                {
                    "weapon_type": "High-Pressure Hydraulic Spreader / Breaching Ram",
                    "confidence": 0.93,
                    "threat_level": "HIGH",
                    "location_in_frame": "Positioned against reinforced steel vault door jamb",
                    "description": "Heavy industrial hydraulic rescue tool adapted for rapid lock displacement"
                }
            ],
            "evidence_tags": [
                {
                    "label": "Discarded Zip-Tie Restraints",
                    "category": "Apparel / Restraint",
                    "confidence": 0.95,
                    "location_in_frame": "Tiled floor near security terminal",
                    "notes": "Heavy-duty 175-lb tensile strength commercial nylon restraints"
                },
                {
                    "label": "Security Alarm Bypass Transponder",
                    "category": "Electronic",
                    "confidence": 0.89,
                    "location_in_frame": "Junction box wall panel adjacent to vault keypad",
                    "notes": "Custom microcontroller board spliced into CAN-bus wiring harness"
                },
                {
                    "label": "Tactical Duffle Bag (Loaded)",
                    "category": "Storage",
                    "confidence": 0.94,
                    "location_in_frame": "Center floor beside vault entryway",
                    "notes": "Large ballistic nylon duffle exhibiting high mass displacement"
                }
            ],
            "scene_environment": {
                "setting": "Bank Sub-Level Main Vault Antechamber",
                "lighting": "Emergency backup fluorescent fixtures operating at 30% nominal lumens",
                "entry_points": ["Reinforced security blast door (breached)", "Ventilation intake shaft (grate removed)"],
                "exit_points": ["Primary security corridor heading toward employee locker area"],
                "security_features_observed": ["Dual-custody time lock mechanism", "Laser tripwire sensor array (bypassed)"],
                "environmental_hazards": ["Hydraulic fluid leak on marble tile", "Airborne aerosolized metal particulate"]
            },
            "forensic_summary": "Interior surveillance capture reveals coordinated forced entry into secure depository. Perpetrators demonstrated specialized breaching tools, lethal firearm posture, and targeted electronics bypass.",
            "overall_confidence": 0.96,
            "is_mock": True
        }

def generate_mock_audio_analysis(filename: str, case_id: str) -> Dict[str, Any]:
    """Generates realistic multimodal forensic audio analysis fallback data."""
    return {
        "case_id": case_id,
        "filename": filename,
        "duration_seconds": 68.5,
        "transcript_segments": [
            {
                "timestamp_start": "00:04.2",
                "timestamp_end": "00:08.7",
                "speaker_label": "Witness / Night Guard",
                "text": "Central dispatch, this is Station 4! I have an unauthorized motion sensor trigger on Level B Vault corridor!",
                "tone_emotion": "Elevated Stress / Urgent"
            },
            {
                "timestamp_start": "00:11.0",
                "timestamp_end": "00:15.8",
                "speaker_label": "Suspect 1 (Perpetrator)",
                "text": "Hands where I can see them! Step back from the console or this goes the hard way!",
                "tone_emotion": "Aggressive / Command Vocalization"
            },
            {
                "timestamp_start": "00:18.2",
                "timestamp_end": "00:22.4",
                "speaker_label": "Suspect 2 (Breacher)",
                "text": "Hydraulic seal is cracked. Give me thirty seconds on the secondary tumblers!",
                "tone_emotion": "Focused / Technical"
            },
            {
                "timestamp_start": "00:29.5",
                "timestamp_end": "00:33.1",
                "speaker_label": "Suspect 1 (Perpetrator)",
                "text": "Grab the deposit boxes in Sector 9, leave the foreign currency. Van is waiting on North Alley!",
                "tone_emotion": "Urgent / Directional"
            },
            {
                "timestamp_start": "00:45.0",
                "timestamp_end": "00:49.2",
                "speaker_label": "Witness / Night Guard",
                "text": "They're heading out the service tunnel... vehicle engine starting up... black Ford transit or SUV!",
                "tone_emotion": "Distressed / Rapid breathing"
            }
        ],
        "extracted_entities": [
            {
                "entity_type": "LOCATION",
                "entity_value": "Level B Vault Corridor",
                "mention_timestamp": "00:06.5",
                "context": "Reported initial point of unauthorized movement"
            },
            {
                "entity_type": "LOCATION",
                "entity_value": "North Alley / Service Tunnel",
                "mention_timestamp": "00:31.0",
                "context": "Identified planned suspect extraction vector"
            },
            {
                "entity_type": "TARGET",
                "entity_value": "Sector 9 Deposit Boxes",
                "mention_timestamp": "00:30.2",
                "context": "Specific high-value target designated by primary suspect"
            },
            {
                "entity_type": "VEHICLE",
                "entity_value": "Black Ford Transit / Full-Size SUV",
                "mention_timestamp": "00:47.8",
                "context": "Getaway vehicle description provided by witness"
            },
            {
                "entity_type": "WEAPON_MENTION",
                "entity_value": "Lethal Force Threat / Firearm",
                "mention_timestamp": "00:13.5",
                "context": "Suspect verbal threat of lethal violence against security personnel"
            }
        ],
        "acoustic_events": [
            {
                "timestamp": "00:09.8",
                "event_type": "Heavy Metallic Impact / Door Kick",
                "confidence": 0.94,
                "decibel_profile": "92 dB peak"
            },
            {
                "timestamp": "00:23.4",
                "event_type": "Hydraulic Pneumatic Release Hiss",
                "confidence": 0.91,
                "decibel_profile": "84 dB steady"
            },
            {
                "timestamp": "00:38.1",
                "event_type": "Shattering Glass / Enclosure Fracture",
                "confidence": 0.96,
                "decibel_profile": "104 dB acute"
            },
            {
                "timestamp": "00:52.0",
                "event_type": "High RPM Engine Acceleration & Tire Squeal",
                "confidence": 0.97,
                "decibel_profile": "96 dB sustained"
            }
        ],
        "forensic_summary": "Acoustic examination establishes a verified timeline of confrontation, forced breach, targeted theft of Sector 9 assets, and motorized vehicular escape via North Alley. Clear vocal separation achieved between guard and multiple perpetrators.",
        "overall_confidence": 0.94,
        "is_mock": True
    }

def generate_mock_video_analysis(filename: str, case_id: str) -> Dict[str, Any]:
    """Generates realistic multimodal forensic video event logs and keyframes."""
    # Ensure sample keyframes exist or generate synthetic ones
    ensure_synthetic_keyframes()
    
    keyframe_events = [
        {
            "timestamp": "00:03.5",
            "action_detected": "Perimeter Breach & Security Camera Spray Tampering",
            "subject_description": "Suspect Alpha approaches CCTV lens with pressurized aerosol can; visual obscuration attempted",
            "scene_location": "External North Alleyway / Loading Dock Gate",
            "confidence": 0.95,
            "severity": "HIGH",
            "keyframe_preview_path": "/static/keyframe_01.jpg"
        },
        {
            "timestamp": "00:14.2",
            "action_detected": "Forced Lock Bypassing & Portal Ingress",
            "subject_description": "Suspect Beta inserts pneumatic pry tool into reinforced door latch; door swings open inward",
            "scene_location": "Door 4B Service Entrance",
            "confidence": 0.98,
            "severity": "CRITICAL",
            "keyframe_preview_path": "/static/keyframe_02.jpg"
        },
        {
            "timestamp": "00:28.0",
            "action_detected": "Weapon Brandishing & Hostile Stance",
            "subject_description": "Suspect Alpha sweeps corridor with drawn firearm; confirms perimeter security guard neutralized",
            "scene_location": "Sub-Level Main Corridor Junction",
            "confidence": 0.97,
            "severity": "CRITICAL",
            "keyframe_preview_path": "/static/keyframe_03.jpg"
        },
        {
            "timestamp": "00:46.8",
            "action_detected": "Vault Door Separation & Asset Retrieval",
            "subject_description": "Suspect Beta pulls open heavy vault door; two large duffle bags filled from safety deposit bins",
            "scene_location": "Main Depository Vault",
            "confidence": 0.96,
            "severity": "CRITICAL",
            "keyframe_preview_path": "/static/keyframe_04.jpg"
        },
        {
            "timestamp": "01:02.1",
            "action_detected": "Rapid Evacuation & Vehicular Boarding",
            "subject_description": "Both suspects run through Door 4B into idling dark minivan; vehicle accelerates immediately north",
            "scene_location": "Loading Dock Curb / Escape Corridor",
            "confidence": 0.93,
            "severity": "HIGH",
            "keyframe_preview_path": "/static/keyframe_05.jpg"
        }
    ]
    
    return {
        "case_id": case_id,
        "filename": filename,
        "duration_seconds": 72.0,
        "keyframe_events": keyframe_events,
        "temporal_summary": "Surveillance video captures full 5-stage felony sequence: initial lens tampering, pneumatic door breach, armed corridor control, asset extraction from depository vault, and synchronized vehicle getaway in under 70 seconds.",
        "detected_actions_count": len(keyframe_events),
        "overall_confidence": 0.96,
        "is_mock": True
    }

def generate_mock_chat_response(case_id: str, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
    """Generates context-aware forensic investigator responses referencing timestamps and evidence."""
    q = query.lower()
    
    if "weapon" in q or "gun" in q or "firearm" in q:
        reply = (
            "Forensic analysis across visual and acoustic feeds confirms **two distinct weapons**:\n\n"
            "1. **Glock 19 / Sig Sauer 9mm Handgun** — Positively identified on Suspect Alpha at `[CAM-01 @ 23:41:15]` "
            "with 97% confidence. Held in Weaver tactical grip.\n"
            "2. **Pneumatic / Hydraulic Spreader & Tactical Crowbar** — Observed at `[CAM-02 @ 23:38:10]` used to breach Door 4B latch.\n\n"
            "Verbal threat logged at `[AUDIO-02 @ 00:11.0]`: *'Hands where I can see them or this goes the hard way!'*"
        )
        citations = [
            {"source": "IMAGE / CAM-01", "timestamp": "23:41:15", "details": "9mm handgun identified in Weaver stance"},
            {"source": "VIDEO / CAM-02", "timestamp": "00:14.2", "details": "Pneumatic lock breach apparatus identified"},
            {"source": "AUDIO / SENSOR-02", "timestamp": "00:11.0", "details": "Verbal threat of lethal force"}
        ]
    elif "timeline" in q or "sequence" in q or "when" in q:
        reply = (
            "Here is the established chronological sequence of the incident:\n\n"
            "- **23:38:10** — Ingress forced via rear service door 4B `[VIDEO @ 00:03.5]`\n"
            "- **23:39:45** — Internal motion sensor B disabled `[VIDEO @ 00:14.2]`\n"
            "- **23:41:15** — Handgun drawn in main corridor `[IMAGE @ 23:41:15]`\n"
            "- **23:41:30** — Vocal threat to night guard recorded `[AUDIO @ 00:11.0]`\n"
            "- **23:42:05** — High impulse acoustic blast (108 dB) vault seal breach `[AUDIO @ 00:23.4]`\n"
            "- **23:44:50** — Extraction of Sector 9 assets in two duffle bags `[VIDEO @ 00:46.8]`\n"
            "- **23:45:20** — Getaway vehicle departure accelerating north `[AUDIO @ 00:52.0]`"
        )
        citations = [
            {"source": "TIMELINE_FUSION", "timestamp": "23:38:10 - 23:45:20", "details": "Master fused chronology"}
        ]
    elif "suspect" in q or "person" in q or "who" in q or "description" in q:
        reply = (
            "We have identified **two active perpetrators** and **one victim/witness**:\n\n"
            "- **Suspect 1 (Alpha)**: ~5'11'', athletic build, matte black Nomex windbreaker, carbon knuckle gloves, "
            "carrying a Glock 19 sidearm. Acts as armed perimeter controller and vocal leader.\n"
            "- **Suspect 2 (Beta)**: ~5'9'', wearing tactical coveralls, welding gloves, and optical goggles. "
            "Operated the hydraulic breaching tools and handled bag packing.\n"
            "- **Victim (Guard)**: Station 4 night security officer, incapacitated near Door 4B corridor."
        )
        citations = [
            {"source": "IMAGE / CAM-01", "timestamp": "23:41:15", "details": "Suspect 1 & 2 biometric and apparel telemetry"},
            {"source": "AUDIO / SENSOR-02", "timestamp": "00:04.2", "details": "Guard radio dispatch audio"}
        ]
    elif "contradiction" in q or "alibi" in q or "witness" in q or "match" in q:
        reply = (
            "**Forensic Discrepancy Alert:**\n\n"
            "1. **Entry Time Discrepancy**: A questioned individual claimed they departed the building at 23:30, "
            "however video telemetry logs unmasked physical presence until `23:44:50`.\n"
            "2. **Vehicle Statement**: Security guard reported a black Ford Transit or SUV, matching the high displacement "
            "V8 engine acoustic signature recorded at `23:45:20`."
        )
        citations = [
            {"source": "VIDEO / CAM-04", "timestamp": "23:44:50", "details": "Visual exit log contradicts early departure statement"},
            {"source": "AUDIO / SENSOR-01", "timestamp": "23:45:20", "details": "Acoustic vehicle signature confirmation"}
        ]
    else:
        reply = (
            f"Based on the fused multimodal evidence for Case `{case_id}`:\n\n"
            "The incident is formally classified as an **Armed Commercial Depository Robbery (Grade 1 Felony)**. "
            "The database currently records multiple synchronized modalities including high-resolution vision snapshots, "
            "multichannel acoustic logs with vocal speaker mapping, and keyframe event tracking.\n\n"
            "You can query specific details such as suspect descriptions, weapon types, entry/exit vectors, or timeline contradictions."
        )
        citations = [
            {"source": "EVIDENCE_DB", "timestamp": "FUSED_STATE", "details": "Case knowledge retrieval"}
        ]
        
    return {
        "case_id": case_id,
        "reply": reply,
        "citations": citations,
        "timestamp": "2026-10-25 21:00:00"
    }

def ensure_synthetic_keyframes():
    """Generates synthetic high-tech forensic keyframe thumbnails for video analysis visual display."""
    target_dir = settings.BACKEND_DIR / "uploads" / "keyframes"
    target_dir.mkdir(parents=True, exist_ok=True)
    
    colors = [
        ("#0f172a", "#38bdf8", "00:03.5 - CAMERA 01 [EXTERIOR ALLEYWAY] - LENS INTERFERENCE"),
        ("#111827", "#f59e0b", "00:14.2 - CAMERA 02 [SERVICE DOOR 4B] - FORCED ENTRY DETECTED"),
        ("#18181b", "#ef4444", "00:28.0 - CAMERA 03 [MAIN CORRIDOR] - WEAPON DETECTED [GLOCK 19]"),
        ("#0f172a", "#10b981", "00:46.8 - CAMERA 04 [VAULT ANTECHAMBER] - REINFORCED BREACH"),
        ("#1e1b4b", "#a855f7", "01:02.1 - CAMERA 05 [EXIT RUNWAY] - ESCAPE VEHICLE BOARDING")
    ]
    
    for i, (bg, accent, text) in enumerate(colors, 1):
        path = target_dir / f"keyframe_{i:02d}.jpg"
        if not path.exists():
            img = Image.new("RGB", (640, 360), color=bg)
            draw = ImageDraw.Draw(img)
            
            # Draw forensic grid
            for x in range(0, 640, 40):
                draw.line([(x, 0), (x, 360)], fill="#1f2937", width=1)
            for y in range(0, 360, 40):
                draw.line([(0, y), (640, y)], fill="#1f2937", width=1)
                
            # Draw tactical HUD bounding box
            draw.rectangle([140, 60, 500, 300], outline=accent, width=2)
            draw.line([(120, 180), (160, 180)], fill=accent, width=2)
            draw.line([(480, 180), (520, 180)], fill=accent, width=2)
            draw.line([(320, 40), (320, 80)], fill=accent, width=2)
            draw.line([(320, 280), (320, 320)], fill=accent, width=2)
            
            # Corner markers
            size = 15
            for cx, cy in [(140, 60), (500, 60), (140, 300), (500, 300)]:
                draw.rectangle([cx - size, cy - size, cx + size, cy + size], outline=accent, width=2)
                
            # Header text and telemetry
            draw.rectangle([0, 0, 640, 32], fill="#030712")
            draw.text((12, 8), f"CRIMEVISION AI HUD // TELEMETRY STREAM // {text}", fill="#ffffff")
            draw.text((12, 335), "CONFIDENCE: 96.8% | CLASSIFICATION: THREAT LEVEL ALPHA | FORENSIC ARCHIVE", fill=accent)
            
            img.save(path, quality=85)
