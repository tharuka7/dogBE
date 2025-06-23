"""## Setup API key"""

import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import json
from PIL import Image
import time
from pathlib import Path

# Load environment variables from .env file
load_dotenv()

# Access the API key
GOOGLE_API_KEY = os.getenv("API_KEY")
if GOOGLE_API_KEY:
    print(f"API Key loaded (first 5 chars): {GOOGLE_API_KEY[:5]}...")
else:
    print("Error: API Key not found in environment variables!")
    exit() # Stop if key isn't found

"""## Initialize SDK client"""
client = genai.Client(api_key=GOOGLE_API_KEY)

def upload_video(video_file_name):
    video_file = client.files.upload(file=video_file_name)

    while video_file.state == "PROCESSING":
        print('Waiting for video to be processed.')
        time.sleep(10)
        video_file = client.files.get(name=video_file.name)

    if video_file.state == "FAILED":
        raise ValueError(video_file.state)
    print(f'states: {video_file.state}')
    print(f'Video processing complete: ' + video_file.uri)
    return video_file

my_file = upload_video('D:\\WORKS ON\\AI-Data Science\\Projects to do\\Project 04\\Project\\Pet_Care_app_BE\\Videos\\a.mp4')

my_custom_prompt = """
**Role:** You are an AI assistant specialized in analyzing animal behavior from video footage. You are tasked with identifying behavioral signs potentially associated with neurological conditions like rabies in dogs, based *only* on the visual information provided. You are NOT a veterinarian and cannot provide a diagnosis.

**Task:** Analyze the provided video clip of a dog. Identify any behaviors exhibited that are commonly listed as potential symptoms of rabies. Based *solely* on the observed behaviors in the video, assess a *potential risk level* (Low, Medium, High) that these behaviors *could be consistent* with rabies symptoms. Provide a concise explanation for your assessment, referencing specific visual evidence.

**Input:** A video clip showing a dog's behavior.

**Analysis Guidelines:**
1.  **Observe Behaviors:** Carefully watch the dog's actions, movements, posture, and any audible sounds if discernible.
2.  **Identify Potential Signs:** Look specifically for behaviors such as:
    *   Unprovoked aggression or unusual irritability
    *   Excessive drooling or foaming at the mouth (hypersalivation)
    *   Difficulty swallowing (dysphagia)
    *   Strange vocalizations (unusual barking, howling, whining)
    *   Stumbling, incoordination, weakness, or paralysis (especially in the hind legs)
    *   Disorientation, confusion, or vacant staring
    *   Restlessness, pacing, or agitation
    *   Seizures
    *   Jaw dropping or facial paralysis
    *   Aversion to water (hydrophobia - rare to capture clearly on video but note any related behavior)
    *   Self-mutilation (biting/chewing at limbs)
3.  **Assess Risk Level:** Based on the presence, combination, and severity of the *observed signs only*:
    *   **Low Risk:** No specific rabies-associated signs observed, or behavior appears normal/explainable by context (e.g., playful barking, normal tiredness).
    *   **Medium Risk:** One or two potential signs observed, but they could also have other causes (e.g., some agitation, slight incoordination that could be an injury). The behavior warrants caution.
    *   **High Risk:** Multiple significant signs strongly associated with rabies are clearly visible (e.g., unprovoked aggression combined with facial paralysis and hypersalivation; severe disorientation with seizures).
4.  **Explain Your Reasoning:** Briefly describe *which specific behaviors* (or lack thereof) led to your risk assessment. Be factual and refer only to what is visible in the video.
5.  **Mandatory Disclaimer:** ALWAYS conclude your explanation with: "Disclaimer: This analysis is based solely on the provided video and is NOT a veterinary diagnosis. Rabies is a serious condition. If you have any concerns about this animal's health or behavior, consult a qualified veterinarian immediately."

**Output Format:** Please provide the response in JSON format with the following keys:
*   `risk_level`: (String: "Low", "Medium", or "High")
*   `explanation`: (String: Your detailed explanation, including the mandatory disclaimer)
*   `observed_signs`: (List of Strings: Specific potential signs observed, e.g., ["Unprovoked aggression", "Hypersalivation"])

**Example Video Input:** [Video Data or Reference to Video Data will be provided here by the API call]
"""

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=[my_file, my_custom_prompt]
)

print(response.text)