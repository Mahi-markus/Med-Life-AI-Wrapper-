import base64
import requests
from PyPDF2 import PdfReader
from dotenv import load_dotenv
import os
import json

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# ...existing code...

def generate_health_plan(health_profile):
    """
    Generate a health plan using Groq AI based on healthProfile data.
    Returns a dict with food_chart, exercise_plan, sleep_plan.
    """
    url = "https://api.groq.com/openai/v1/chat/completions"

    user_content = f"""
    Generate a personalized health plan based on the following profile data.

    Profile:
    - Age: {health_profile.age}
    - Weight: {health_profile.weight} kg
    - Height: {health_profile.height_feet} feet {health_profile.height_inches} inches
    - BMI: {health_profile.bmi}
    - Disease: {health_profile.disease}
    - Additional Info: {health_profile.addition_info or 'None'}

    Return ONLY valid JSON. No explanation.

    JSON FORMAT:
    {{
        "food_chart": "string (detailed daily meal plan)",
        "exercise_plan": "string (recommended exercises and routine)",
        "sleep_plan": "string (sleep recommendations)"
    }}
    """

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {
                "role": "system",
                "content": "You generate personalized health plans into clean JSON."
            },
            {
                "role": "user",
                "content": user_content
            }
        ]
    }

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    data = response.json()

    if "choices" not in data or not data["choices"]:
        raise ValueError(f"AI API Error: {data}")

    raw = data["choices"][0]["message"]["content"]
    if raw.startswith("```"):
        raw = raw.strip().replace("```json", "").replace("```", "").strip()

    return json.loads(raw)




# ...existing code...


def generate_dietry_recommendation(health_profile):
    """
    Generate dietary recommendations using Groq AI based on healthProfile data.
    Returns a dict with breakfast, lunch, dinner recommendations.
    """
    url = "https://api.groq.com/openai/v1/chat/completions"

    user_content = f"""
    Generate dietary recommendations for breakfast, lunch, and dinner based on the following health profile:

    - Age: {health_profile.age}
    - Weight: {health_profile.weight} kg
    - Height: {health_profile.height_feet} feet {health_profile.height_inches} inches
    - BMI: {health_profile.bmi}
    - Disease: {health_profile.disease}
    - Additional Info: {health_profile.addition_info or 'None'}

    Return ONLY valid JSON in the following format:
    {{
        "breakfast": "string (recommended breakfast foods)",
        "lunch": "string (recommended lunch foods)",
        "dinner": "string (recommended dinner foods)",
        "snacks": "string (recommended snacks, optional)",
        "food_to_avoid": "string (foods to avoid, optional)"
    }}
    """
    payload = {
    "model": "llama-3.3-70b-versatile",
    "messages": [
        {
            "role": "system",
            "content": "You generate personalized health plans into clean JSON."
        },
        {
            "role": "user",
            "content": user_content
        }
    ]
}

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    data = response.json()

    if "choices" not in data or not data["choices"]:
        raise ValueError(f"AI API Error: {data}")

    raw = data["choices"][0]["message"]["content"]
    if raw.startswith("```"):
        raw = raw.strip().replace("```json", "").replace("```", "").strip()

    return json.loads(raw)
