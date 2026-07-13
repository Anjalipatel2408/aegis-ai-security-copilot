import os
import shutil
from datetime import datetime

# Current file (log_service.py) ના location ના આધારે absolute path બનાવો
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # app/ folder
UPLOAD_DIR = os.path.join(BASE_DIR, "uploaded_logs")

def save_uploaded_file(file):
    os.makedirs(UPLOAD_DIR, exist_ok=True)  # દર વખતે call કરો, error-safe

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    safe_filename = f"{timestamp}_{file.filename}"
    file_location = os.path.join(UPLOAD_DIR, safe_filename)

    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    file_size = os.path.getsize(file_location)

    return file_location, file_size