from fastapi import FastAPI
from app.database import Base, engine
from app.models.log_model import LogFile
from app.routes.log_routes import router as log_router
from app.models.parsed_log_model import ParsedLogEntry
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="AEGIS AI Security Copilot")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
Base.metadata.create_all(bind=engine)
app.include_router(log_router)

@app.get("/health")
def health_check():
    return {"status": "OK", "service": "AEGIS AI"}

@app.get("/test-db")
def test_db_connection():
    from app.database import engine
    try:
        conn = engine.connect()
        conn.close()
        return {"database": "Connected successfully!"}
    except Exception as e:
        return {"database": "Connection failed", "error": str(e)}