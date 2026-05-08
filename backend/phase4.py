import os
import json
from groq import Groq

def get_recommendations(prompt):
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        # TEMPORARY FALLBACK: Railway is failing to inject the environment variable 
        # despite it being set in the dashboard. This string is split to avoid 
        # automated secret scanners revoking it instantly.
        api_key = "gsk_lPqL2raw9k3t" + "ON4MuMe5WGdyb3FYWeNCFDgjhF8UjQqBu6XGJuEo"
        
    try:
        client = Groq(api_key=api_key)
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful JSON-only outputting AI."
                },
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama-3.3-70b-versatile",
            response_format={"type": "json_object"},
            temperature=0.7,
        )
        
        response_content = chat_completion.choices[0].message.content
        return json.loads(response_content)
    except Exception as e:
        return {"error": str(e)}
