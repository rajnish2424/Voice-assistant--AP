from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from supabase_client import get_clients
from voice_engine import generate_response_audio, call_via_agora
import os

app = FastAPI(
    title="Voice Agent API",
    description="Handles customer callbacks using Supabase + Voice APIs.",
    version="0.1.0"
)

# ✅ Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to frontend domain
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

        # 🔍 Find the client by phone number
        matched = next(
            (row for row in all_records if str(row.get("phone")) == request.phone_number),
            None
        )

        if not matched:
            return {"status": "not_found", "message": "Phone number not found in database."}

        # 🗣 Generate message based on language
        if request.language.lower() == "hindi":
            message = f"नमस्ते {matched.get('name', 'ग्राहक')}, हमने देखा कि इस महीने आपके खर्च कम हो गए हैं। क्या आप सलाहकार से बात करना चाहेंगे?"
        else:
            message = f"Hello {matched.get('name', 'there')}, we noticed your monthly expenses have dropped. Would you like to speak with an advisor?"

        # 🔊 Generate voice audio
        audio_file_path = generate_response_audio(message, language=request.language)

        # 📞 Trigger voice call (stub for now)
        call_triggered = call_via_agora(request.phone_number, audio_file_path)

        return {
            "status": "call_triggered" if call_triggered else "call_failed",
            "customer_name": matched.get("name", "Unknown"),
            "phone": request.phone_number,
            "language": request.language,
            "audio_file": audio_file_path
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}

# ✅ For Render deployment: ensure Uvicorn starts from this file
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    print(f"✅ Voice Agent Backend is running on port {port}")
    uvicorn.run("main:app", host="0.0.0.0", port=port)
