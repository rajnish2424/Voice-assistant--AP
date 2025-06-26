from fastapi import FastAPI
from pydantic import BaseModel
from google_sheets import get_sheet
import os

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Voice Agent Backend is running!"}

class CallRequest(BaseModel):
    customer_id: str
    language: str = "english"

@app.post("/start-call")
def start_call(request: CallRequest):
    try:
        sheet = get_sheet()
        all_records = sheet.get_all_records()

        # Find the customer row
        matched = next((row for row in all_records if str(row.get("CustomerID")) == request.customer_id), None)
        if not matched:
            return {"error": "Customer not found"}

        # Placeholder logic to trigger call
        return {
            "status": "call triggered",
            "customer_id": request.customer_id,
            "language": request.language,
            "customer_name": matched.get("Name", "Unknown")
        }

    except Exception as e:
        return {"error": str(e)}
