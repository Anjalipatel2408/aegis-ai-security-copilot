import os
from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.log_model import LogFile
from app.services.log_service import save_uploaded_file
from app.models.parsed_log_model import ParsedLogEntry
from app.services.log_parser import parse_log_file
from app.services.anomaly_detector import detect_anomalies
from app.services.attack_classifier import classify_attack
from app.services.llm_service import get_remediation_advice
from app.services.pdf_report import generate_incident_report
from app.services.email_service import send_alert_email
from fastapi.responses import FileResponse

router = APIRouter()

@router.post("/upload-log")
def upload_log(file: UploadFile = File(...), db: Session = Depends(get_db)):
    file_path, file_size = save_uploaded_file(file)

    log_entry = LogFile(
        filename=file.filename,
        file_path=file_path,
        file_size=file_size,
        status="uploaded"
    )
    db.add(log_entry)
    db.commit()
    db.refresh(log_entry)

    return {
        "message": "File uploaded successfully",
        "log_id": log_entry.id,
        "filename": log_entry.filename,
        "size": log_entry.file_size
    }

@router.get("/logs")
def get_all_logs(db: Session = Depends(get_db)):
    logs = db.query(LogFile).all()
    return logs
@router.post("/parse-log/{log_id}")
def parse_log(log_id: int, db: Session = Depends(get_db)):
    log_file = db.query(LogFile).filter(LogFile.id == log_id).first()
    if not log_file:
        return {"error": "Log file not found"}

    parsed_entries = parse_log_file(log_file.file_path)

    for entry in parsed_entries:
        db_entry = ParsedLogEntry(
            log_file_id=log_file.id,
            timestamp=entry["timestamp"],
            level=entry["level"],
            ip_address=entry["ip_address"],
            method=entry["method"],
            endpoint=entry["endpoint"],
            status_code=entry["status_code"],
            raw_line=entry["raw_line"]
        )
        db.add(db_entry)

    log_file.status = "parsed"
    db.commit()

    return {
        "message": "Log parsed successfully",
        "total_entries": len(parsed_entries)
    }

@router.get("/parsed-logs/{log_id}")
def get_parsed_logs(log_id: int, db: Session = Depends(get_db)):
    entries = db.query(ParsedLogEntry).filter(ParsedLogEntry.log_file_id == log_id).all()
    return entries
@router.post("/detect-anomalies/{log_id}")
def detect_log_anomalies(log_id: int, db: Session = Depends(get_db)):
    entries = db.query(ParsedLogEntry).filter(ParsedLogEntry.log_file_id == log_id).all()

    if not entries:
        return {"error": "No parsed entries found. Parse the log first."}

    results = detect_anomalies(entries)

    anomaly_count = 0
    for entry in entries:
        score = results.get(entry.id, 1)
        entry.anomaly_score = int(score)
        if score == -1:
            anomaly_count += 1

    db.commit()

    return {
        "message": "Anomaly detection completed",
        "total_entries": len(entries),
        "anomalies_found": anomaly_count
    }

@router.get("/anomalies/{log_id}")
def get_anomalies(log_id: int, db: Session = Depends(get_db)):
    anomalies = db.query(ParsedLogEntry).filter(
        ParsedLogEntry.log_file_id == log_id,
        ParsedLogEntry.anomaly_score == -1
    ).all()
    return anomalies
@router.post("/classify-attacks/{log_id}")
def classify_attacks(log_id: int, db: Session = Depends(get_db)):
    all_entries = db.query(ParsedLogEntry).filter(ParsedLogEntry.log_file_id == log_id).all()
    anomalies = [e for e in all_entries if e.anomaly_score == -1]

    if not anomalies:
        return {"error": "No anomalies found. Run anomaly detection first."}

    for entry in anomalies:
        result = classify_attack(entry, all_entries)
        entry.attack_type = result["attack_type"]
        entry.mitre_technique_id = result["mitre_technique_id"]
        entry.mitre_technique_name = result["mitre_technique_name"]
        entry.mitre_tactic = result["mitre_tactic"]

    db.commit()

    return {
        "message": "Attack classification completed",
        "classified_count": len(anomalies)
    }

@router.get("/attack-summary/{log_id}")
def get_attack_summary(log_id: int, db: Session = Depends(get_db)):
    anomalies = db.query(ParsedLogEntry).filter(
        ParsedLogEntry.log_file_id == log_id,
        ParsedLogEntry.anomaly_score == -1
    ).all()

    return [
        {
            "id": e.id,
            "ip_address": e.ip_address,
            "endpoint": e.endpoint,
            "attack_type": e.attack_type,
            "mitre_technique_id": e.mitre_technique_id,
            "mitre_technique_name": e.mitre_technique_name,
            "mitre_tactic": e.mitre_tactic
        }
        for e in anomalies
    ]
@router.get("/remediation/{entry_id}")
def get_remediation(entry_id: int, db: Session = Depends(get_db)):
    entry = db.query(ParsedLogEntry).filter(ParsedLogEntry.id == entry_id).first()

    if not entry:
        return {"error": "Log entry not found"}

    advice = get_remediation_advice(
        attack_type=entry.attack_type or "Unknown",
        mitre_technique=f"{entry.mitre_technique_id} - {entry.mitre_technique_name}",
        ip_address=entry.ip_address or "Unknown",
        endpoint=entry.endpoint or "Unknown"
    )

    return {
        "entry_id": entry.id,
        "attack_type": entry.attack_type,
        "remediation_advice": advice
    }
@router.get("/generate-report/{log_id}")
def generate_report(log_id: int, db: Session = Depends(get_db)):
    log_file = db.query(LogFile).filter(LogFile.id == log_id).first()
    attacks_query = db.query(ParsedLogEntry).filter(
        ParsedLogEntry.log_file_id == log_id,
        ParsedLogEntry.anomaly_score == -1
    ).all()

    attacks = [
        {
            "ip_address": a.ip_address,
            "endpoint": a.endpoint,
            "attack_type": a.attack_type,
            "mitre_technique_id": a.mitre_technique_id,
            "mitre_technique_name": a.mitre_technique_name
        }
        for a in attacks_query
    ]

    file_path = generate_incident_report(log_file.filename, attacks)
    return FileResponse(file_path, media_type="application/pdf", filename=os.path.basename(file_path))

@router.post("/send-alert/{log_id}")
def send_alert(log_id: int, to_email: str, db: Session = Depends(get_db)):
    attack_count = db.query(ParsedLogEntry).filter(
        ParsedLogEntry.log_file_id == log_id,
        ParsedLogEntry.anomaly_score == -1
    ).count()

    result = send_alert_email(
        to_email=to_email,
        subject=f"AEGIS AI Alert: {attack_count} threats detected",
        body=f"AEGIS AI detected {attack_count} potential security threats in log ID {log_id}. Please review the dashboard immediately."
    )
    return result