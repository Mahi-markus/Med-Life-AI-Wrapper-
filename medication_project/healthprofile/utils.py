import requests
from .models import healthProfile,HealthPlan

def build_health_prompt(profile):
    prompt = f"""
    Patient: {profile.patient.name}, Age: {profile.age} years,
    Weight: {profile.weight} kg, Height: {profile.height} m,
    Disease: {profile.disease}.
    Additional info: {profile.addition_info or 'None'}.

    Based on this health profile, create:
    1. A food chart (healthy diet)
    2. An exercise plan suitable for the patient
    3. A sleep plan if necessary
    Write it in clear, structured text.
    """
    return prompt

def generate_health_plan(profile):
    prompt = build_health_prompt(profile)
    api_url =  f"https://text.pollinations.ai/{requests.utils.quote(prompt)}"
    response = requests.get(api_url)
    if response.status_code == 200:
        plain_text = response.text
        print(plain_text)
        return plain_text
    else:
        print(f"Error: {response.status_code}")
        return "Could not generate health plan at this time."
