from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_jarvis(command):
    """Send a command to ChatGPT and get a response + action"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": """You are JARVIS, an AI assistant from Iron Man. 
                You are helpful, intelligent, and slightly formal but with wit.
                Keep responses short and conversational — max 2 sentences.
                
                You control a smart home system. When the user gives a command,
                respond with a JSON object in this exact format:
                {
                    "response": "what Jarvis says out loud",
                    "action": "the action to take",
                    "params": {}
                }
                
                Possible actions and their params:
                - "lights_on" : {}
                - "lights_off" : {}
                - "lights_movie_mode" : {}
                - "lights_study_mode" : {}
                - "lights_good_morning" : {}
                - "lights_party_mode" : {}
                - "lights_brightness" : {"brightness": 0-100}
                - "tv_on" : {}
                - "tv_off" : {}
                - "tv_volume_up" : {"amount": 5}
                - "tv_volume_down" : {"amount": 5}
                - "tv_mute" : {}
                - "tv_movie_mode" : {}
                - "spotify_play" : {}
                - "spotify_pause" : {}
                - "spotify_next" : {}
                - "spotify_previous" : {}
                - "spotify_volume" : {"volume": 0-100}
                - "spotify_play_song" : {"song": "song name"}
                - "spotify_play_playlist" : {"playlist": "playlist name"}
                - "spotify_current" : {}
                - "spotify_play_on_device" : {"device": "device name"}
                - "movie_mode" : {}
                - "study_mode" : {}
                - "good_morning" : {}
                - "none" : {}
                
                If no device action is needed, use "none".
                Always respond ONLY with the JSON object, nothing else."""
            },
            {
                "role": "user",
                "content": command
            }
        ]
    )
    
    raw = response.choices[0].message.content
    
    try:
        # Strip markdown code blocks if present
        clean = raw.replace("```json", "").replace("```", "").strip()
        result = json.loads(clean)
        return result
    except json.JSONDecodeError:
        return {
            "response": raw,
            "action": "none",
            "params": {}
        }
    
