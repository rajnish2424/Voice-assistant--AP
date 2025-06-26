from fastapi import FastAPI
from pydantic import BaseModel
import os

app = FastAPI()

# Health check route
@app.get("/")
def read_root():
    return {"message": "Voice Agent Backend is running!"}

# Define request model for the call
class CallRequest(BaseModel):
    customer_id: str
    language: str = "english"

# POST endpoint to trigger call
@app.post("/start-call")
def start_call(request: CallRequest):
    # For now, return this placeholder
    return {
        "status": "call triggered",
        "customer_id": request.customer_id,
        "language": request.language
    }

# Entry point for local/Render execution
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))  # Render provides this env var
    uvicorn.run(app, host="0.0.0.0", port=port)
