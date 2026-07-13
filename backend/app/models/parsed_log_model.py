from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.database import Base

class ParsedLogEntry(Base):
    __tablename__ = "parsed_log_entries"

    id = Column(Integer, primary_key=True, index=True)
    log_file_id = Column(Integer, ForeignKey("log_files.id"))
    timestamp = Column(DateTime, nullable=True)
    level = Column(String, nullable=True)
    ip_address = Column(String, nullable=True)
    method = Column(String, nullable=True)
    endpoint = Column(String, nullable=True)
    status_code = Column(String, nullable=True)
    anomaly_score = Column(Integer, nullable=True)  # -1 = anomaly, 1 = normal
    raw_line = Column(String, nullable=True)
    attack_type = Column(String, nullable=True)
    mitre_technique_id = Column(String, nullable=True)
    mitre_technique_name = Column(String, nullable=True)
    mitre_tactic = Column(String, nullable=True)