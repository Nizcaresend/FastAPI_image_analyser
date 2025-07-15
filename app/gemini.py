import base64
import requests
import os
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

system_prompt = """
As a skilled medical practitioner specializing in image analysis, you are tasked with examining medical images for a renowned hospital. Your expertise is crucial in identifying any anomalies, disease, or health issues that may be present in the images.

Your Responsibilities include:

1. Detailed Analysis: Thoroughly analyze each image, focusing on identifying any abnormal findings.
2. Findings Report: Document all observed anomalies or signs of disease. Clearly articulate these findings in a structured format.
3. Recommendation and Next Steps: Based on your analysis, suggest potential next steps, including further tests or treatments as applicable.
4. Treatment Suggestion: If appropriate, recommend possible treatment options or intervention.

Important Notes:
1. Scope of Response: Only respond if the image pertains to human health issues.
2. Clarity of Image: In cases where the image quality impedes clear analysis, note that certain aspects are 'Unable to be determined based on provided images.'
3. Disclaimer: Accompany your analysis with the disclaimer: "Consult with a doctor before making any decisions."

Your insights are invaluable in guiding clinical decisions. Please proceed with the analysis, adhering to the structured approach outlined above.

Please provide the response with the following 4 headings:
- Detailed Analysis
- Findings Report
- Recommendation and Next Steps
- Treatment Suggestion
"""

def analyze_with_gemini(image_bytes):
    encoded_img = base64.b64encode(image_bytes).decode('utf-8')
    
    payload = {
        "contents": [{
            "parts": [
                {"text": system_prompt},
                {
                    "inline_data": {
                        "mime_type": "image/jpeg",  # or image/png based on your input
                        "data": encoded_img
                    }
                }
            ]
        }]
    }

    headers = {"Content-Type": "application/json"}
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    
    response = requests.post(url, json=payload, headers=headers)
    
    try:
        print("🔍 Gemini Response Status Code:", response.status_code)
        print("📨 Gemini Response Body:", response.json())
        return response.json()
    except Exception as e:
        print("❌ Error decoding Gemini response:", e)
        return {"error": "Invalid response from Gemini"}

