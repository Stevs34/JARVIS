from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_jarvis(command):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": """You are JARVIS, an AI assistant from Iron Man. 
                You are helpful, intelligent, and slightly formal but with wit.
                Keep responses short and conversational — max 2-3 sentences.
                You control a smart home system with lights, TV, and Spotify."""
            },
            {
                "role": "user",
                "content": command
            }
        ]
    )
    return response.choices[0].message.content