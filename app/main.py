from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from app.gemini import analyze_with_gemini
import os
from dotenv import load_dotenv

app = FastAPI()

# Allow Laravel origin if needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change to specific domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/test-key")
def test_key():
    load_dotenv()
    key = os.getenv("GEMINI_API_KEY")
    return {"key": key}

@app.post("/analyze-image/")
async def analyze_image(file: UploadFile = File(...)):
    image_bytes = await file.read()
    result = analyze_with_gemini(image_bytes)

    print("📨 RAW GEMINI RESPONSE:", result)  # ← Add this line

    try:
        text = result['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        print("❌ ERROR PARSING GEMINI RESPONSE:", e)
        text = "Unable to extract analysis."

    return {"summary": text}


