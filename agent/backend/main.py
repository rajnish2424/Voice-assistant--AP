from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from google_sheets import get_sheet
import os

app = FastAPI(
    title="Voice Agent API",
    description="Handles customer callbacks using Google Sheets + Voice APIs.",
    version="0.1.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, set to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {"message": "Voice Agent Backend is running!"}

class CallRequest(BaseModel):
    phone_number: str
    language: str = "english"

@app.post("/start-call")
def start_call(request: CallRequest):
    try:
        sheet = get_sheet()
        all_records = sheet.get_all_records()

        # Find the client by phone number
        matched = next(
            (row for row in all_records if str(row.get("Phone")) == request.phone_number),
            None
        )

        if not matched:
            return {"status": "not_found", "message": "Phone number not found in sheet."}

        # Placeholder: You can trigger Agora/Coqui logic here
        return {
            "status": "call_triggered",
            "customer_name": matched.get("Name", "Unknown"),
            "phone": request.phone_number,
            "language": request.language
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}
