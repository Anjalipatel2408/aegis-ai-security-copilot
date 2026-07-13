from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.database import Base

class LogFile(Base):
    __tablename__ = "log_files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    upload_time = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="uploaded")
    file_size = Column(Integer, nullable=True)