import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from .config import settings

def get_db_connection():
    conn = sqlite3.connect(str(settings.DATABASE_PATH), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. Cases table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cases (
        case_id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        incident_type TEXT NOT NULL,
        location TEXT NOT NULL,
        incident_date TEXT NOT NULL,
        investigator TEXT NOT NULL,
        status TEXT DEFAULT 'ACTIVE',
        severity TEXT DEFAULT 'HIGH',
        summary TEXT,
        created_at TEXT NOT NULL
    )
    """)
    
    # 2. Evidence items table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS evidence (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        case_id TEXT NOT NULL,
        evidence_type TEXT NOT NULL,
        filename TEXT NOT NULL,
        file_path TEXT NOT NULL,
        file_size INTEGER DEFAULT 0,
        mime_type TEXT,
        analysis_json TEXT,
        uploaded_at TEXT NOT NULL,
        FOREIGN KEY (case_id) REFERENCES cases (case_id) ON DELETE CASCADE
    )
    """)
    
    # 3. Timeline events table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS timeline_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        case_id TEXT NOT NULL,
        timestamp_marker TEXT NOT NULL,
        source_modality TEXT NOT NULL,
        event_type TEXT NOT NULL,
        description TEXT NOT NULL,
        confidence REAL DEFAULT 0.95,
        entities_involved TEXT,
        severity TEXT DEFAULT 'MEDIUM',
        created_at TEXT NOT NULL,
        FOREIGN KEY (case_id) REFERENCES cases (case_id) ON DELETE CASCADE
    )
    """)
    
    # 4. Chat history table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chat_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        case_id TEXT NOT NULL,
        sender TEXT NOT NULL,
        message TEXT NOT NULL,
        citations_json TEXT,
        timestamp TEXT NOT NULL,
        FOREIGN KEY (case_id) REFERENCES cases (case_id) ON DELETE CASCADE
    )
    """)
    
    conn.commit()
    conn.close()
    
    # Seed default demonstration cases if DB is brand new
    seed_default_cases()

def seed_default_cases():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) as count FROM cases")
    row = cursor.fetchone()
    if row and row["count"] > 0:
        conn.close()
        return

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Seed Flagship Case
    cursor.execute("""
    INSERT INTO cases (case_id, title, incident_type, location, incident_date, investigator, status, severity, summary, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        "CASE-2026-0891",
        "Metro Central Bank Vault Breach & Armed Robbery",
        "Armed Robbery / Commercial Burglary",
        "Financial District Branch #4, 102 Wall St, New York",
        "2026-10-24 23:40:00",
        "Det. Marcus Vance (Forensic Unit 4)",
        "ACTIVE",
        "CRITICAL",
        "Multimodal forensic inquiry into coordinated night-shift vault breach by two masked perpetrators utilizing tactical thermal lances and semi-automatic weapons.",
        now
    ))
    
    # Seed Secondary Case
    cursor.execute("""
    INSERT INTO cases (case_id, title, incident_type, location, incident_date, investigator, status, severity, summary, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        "CASE-2026-0412",
        "Docklands Pier 19 Warehouse Intrusion",
        "Aggravated Trespassing / Grand Larceny",
        "Industrial Pier 19, South Docks Warehouse B",
        "2026-10-23 02:15:00",
        "Inspector Sarah Chen",
        "UNDER_REVIEW",
        "HIGH",
        "Perimeter breach and high-value electronics container burglary with audible security confrontation and vehicle escape.",
        now
    ))

    # Pre-seed initial timeline events for CASE-2026-0891
    seed_timeline = [
        ("CASE-2026-0891", "23:38:10", "VIDEO", "ENTRY", "Perpetrator 1 (Tactical Gear) forces rear service door lock using magnetic bypass tool.", 0.96, "Perpetrator 1, Rear Service Door", "HIGH", now),
        ("CASE-2026-0891", "23:39:45", "VIDEO", "PERIMETER_PROBE", "Perpetrator 2 disabled internal motion sensor with infrared spray.", 0.92, "Perpetrator 2, Motion Sensor B", "MEDIUM", now),
        ("CASE-2026-0891", "23:41:15", "IMAGE", "WEAPON_DRAWN", "High-resolution snapshot captures Perpetrator 1 drawing Glock 19 9mm pistol in main lobby corridor.", 0.98, "Perpetrator 1, Glock 19", "CRITICAL", now),
        ("CASE-2026-0891", "23:41:30", "AUDIO", "VERBAL_THREAT", "Audio sensor 02 captures vocal command: 'Get on the floor, security code in five seconds!'", 0.95, "Suspect 1, Night Guard", "CRITICAL", now),
        ("CASE-2026-0891", "23:42:05", "AUDIO", "ACOUSTIC_DISTURBANCE", "High acoustic impulse detected (108 dB) consistent with hydraulic vault door lock detonation.", 0.94, "Vault Door, Explosive/Pneumatic tool", "CRITICAL", now),
        ("CASE-2026-0891", "23:44:50", "VIDEO", "EXTRACTION", "Perpetrators 1 & 2 exit carrying two heavy tactical duffle bags toward North Alley.", 0.97, "Perpetrator 1, Perpetrator 2, North Alley", "HIGH", now),
        ("CASE-2026-0891", "23:45:20", "AUDIO", "VEHICLE_DEPARTURE", "Audio microphone records rapid tire friction and high-displacement V8 engine accelerating north.", 0.89, "Getaway Vehicle, North Ave", "MEDIUM", now),
    ]
    cursor.executemany("""
    INSERT INTO timeline_events (case_id, timestamp_marker, source_modality, event_type, description, confidence, entities_involved, severity, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, seed_timeline)

    # Pre-seed initial chat history
    seed_chat = [
        ("CASE-2026-0891", "investigator", "What weapons were detected on scene during the vault breach?", "[]", now),
        ("CASE-2026-0891", "ai_copilot", "Based on visual evidence [CAM-01 @ 23:41:15] and acoustic logs [AUDIO-02 @ 23:41:30], Perpetrator 1 was positively identified carrying a Glock 19 semi-automatic 9mm handgun (98% confidence). Furthermore, thermal acoustic signatures at 23:42:05 confirm a pneumatic/hydraulic vault breach apparatus.", json.dumps([{"source": "IMAGE", "timestamp": "23:41:15", "details": "Glock 19 detected"}, {"source": "AUDIO", "timestamp": "23:42:05", "details": "Detonation impulse"}]), now),
    ]
    cursor.executemany("""
    INSERT INTO chat_history (case_id, sender, message, citations_json, timestamp)
    VALUES (?, ?, ?, ?, ?)
    """, seed_chat)

    conn.commit()
    conn.close()

# Database Query Helper Functions
def get_cases() -> List[Dict[str, Any]]:
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM cases ORDER BY created_at DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_case_by_id(case_id: str) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    row = conn.execute("SELECT * FROM cases WHERE case_id = ?", (case_id,)).fetchone()
    conn.close()
    return dict(row) if row else None

def create_case(case_data: Dict[str, Any]) -> Dict[str, Any]:
    conn = get_db_connection()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn.execute("""
    INSERT INTO cases (case_id, title, incident_type, location, incident_date, investigator, status, severity, summary, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        case_data.get("case_id"),
        case_data.get("title"),
        case_data.get("incident_type"),
        case_data.get("location"),
        case_data.get("incident_date", now),
        case_data.get("investigator", "Chief Investigator"),
        case_data.get("status", "ACTIVE"),
        case_data.get("severity", "HIGH"),
        case_data.get("summary", ""),
        now
    ))
    conn.commit()
    conn.close()
    return get_case_by_id(case_data.get("case_id"))

def add_evidence(case_id: str, evidence_type: str, filename: str, file_path: str, file_size: int, mime_type: str, analysis_json: Dict[str, Any]) -> int:
    conn = get_db_connection()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO evidence (case_id, evidence_type, filename, file_path, file_size, mime_type, analysis_json, uploaded_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        case_id,
        evidence_type,
        filename,
        file_path,
        file_size,
        mime_type,
        json.dumps(analysis_json),
        now
    ))
    evidence_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return evidence_id

def get_evidence_for_case(case_id: str, evidence_type: Optional[str] = None) -> List[Dict[str, Any]]:
    conn = get_db_connection()
    if evidence_type:
        rows = conn.execute("SELECT * FROM evidence WHERE case_id = ? AND evidence_type = ? ORDER BY uploaded_at DESC", (case_id, evidence_type)).fetchall()
    else:
        rows = conn.execute("SELECT * FROM evidence WHERE case_id = ? ORDER BY uploaded_at DESC", (case_id,)).fetchall()
    conn.close()
    res = []
    for r in rows:
        d = dict(r)
        if d.get("analysis_json"):
            try:
                d["analysis_data"] = json.loads(d["analysis_json"])
            except Exception:
                d["analysis_data"] = {}
        res.append(d)
    return res

def add_timeline_event(case_id: str, timestamp_marker: str, source_modality: str, event_type: str, description: str, confidence: float, entities_involved: str, severity: str = "MEDIUM") -> int:
    conn = get_db_connection()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO timeline_events (case_id, timestamp_marker, source_modality, event_type, description, confidence, entities_involved, severity, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        case_id,
        timestamp_marker,
        source_modality,
        event_type,
        description,
        confidence,
        entities_involved,
        severity,
        now
    ))
    ev_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return ev_id

def get_timeline_for_case(case_id: str) -> List[Dict[str, Any]]:
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM timeline_events WHERE case_id = ? ORDER BY timestamp_marker ASC, id ASC", (case_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def clear_timeline_for_case(case_id: str):
    conn = get_db_connection()
    conn.execute("DELETE FROM timeline_events WHERE case_id = ?", (case_id,))
    conn.commit()
    conn.close()

def add_chat_message(case_id: str, sender: str, message: str, citations: List[Dict[str, Any]] = None) -> int:
    conn = get_db_connection()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO chat_history (case_id, sender, message, citations_json, timestamp)
    VALUES (?, ?, ?, ?, ?)
    """, (
        case_id,
        sender,
        message,
        json.dumps(citations or []),
        now
    ))
    msg_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return msg_id

def get_chat_history(case_id: str) -> List[Dict[str, Any]]:
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM chat_history WHERE case_id = ? ORDER BY id ASC", (case_id,)).fetchall()
    conn.close()
    res = []
    for r in rows:
        d = dict(r)
        if d.get("citations_json"):
            try:
                d["citations"] = json.loads(d["citations_json"])
            except Exception:
                d["citations"] = []
        res.append(d)
    return res

def get_case_statistics(case_id: str) -> Dict[str, Any]:
    conn = get_db_connection()
    ev_counts = conn.execute("""
    SELECT evidence_type, COUNT(*) as count 
    FROM evidence WHERE case_id = ? GROUP BY evidence_type
    """, (case_id,)).fetchall()
    
    tl_count = conn.execute("SELECT COUNT(*) as count FROM timeline_events WHERE case_id = ?", (case_id,)).fetchone()["count"]
    crit_count = conn.execute("SELECT COUNT(*) as count FROM timeline_events WHERE case_id = ? AND severity = 'CRITICAL'", (case_id,)).fetchone()["count"]
    chat_count = conn.execute("SELECT COUNT(*) as count FROM chat_history WHERE case_id = ?", (case_id,)).fetchone()["count"]
    case_info = conn.execute("SELECT * FROM cases WHERE case_id = ?", (case_id,)).fetchone()
    conn.close()
    
    counts_map = {row["evidence_type"]: row["count"] for row in ev_counts}
    
    return {
        "case_id": case_id,
        "case_title": case_info["title"] if case_info else "Unknown",
        "case_status": case_info["status"] if case_info else "ACTIVE",
        "case_severity": case_info["severity"] if case_info else "HIGH",
        "images_count": counts_map.get("IMAGE", 0),
        "audio_count": counts_map.get("AUDIO", 0),
        "video_count": counts_map.get("VIDEO", 0),
        "total_evidence": sum(counts_map.values()),
        "timeline_events_count": tl_count,
        "critical_alerts_count": crit_count,
        "chat_queries_count": chat_count
    }
