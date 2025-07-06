from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from supabase_client import get_clients
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
        all_records = get_clients()

        # Find the client by phone number
        matched = next(
            (row for row in all_records if str(row.get("phone")) == request.phone_number),
            None
        )

        if not matched:
            return {"status": "not_found", "message": "Phone number not found in database."}

        # Trigger voice agent logic here if match is found
        return {
            "status": "call_triggered",
            "customer_name": matched.get("name", "Unknown"),
            "phone": request.phone_number,
            "language": request.language
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}

# ✅ Start FastAPI with uvicorn so Render can detect the port
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    print(f"✅ Voice Agent Backend is running on port {port}")
    uvicorn.run("main:app", host="0.0.0.0", port=port)
