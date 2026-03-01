from openai import OpenAI
from dotenv import load_dotenv
from memory import get_memory_context
import os
import json

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Store conversation history for more natural multi-turn conversation
conversation_history = []
MAX_HISTORY = 10

def ask_jarvis(command):
    """Send a command to ChatGPT with memory and conversation history"""
    global conversation_history

    memory_context = get_memory_context()

    system_prompt = f"""You are JARVIS, an AI assistant from Iron Man. 
    You are helpful, intelligent, slightly formal but with wit and personality.
    You address the user as "sir" occasionally but not every sentence.
    Keep responses short and conversational — max 2 sentences unless asked for more detail.
    You have been with this user for a while and know them well.
    
    Here is what you know about the user:
    {memory_context}
    
    You control a smart home system. When the user gives a command,
    respond with a JSON object in this exact format:
    {{
        "response": "what Jarvis says out loud",
        "action": "the action to take",
        "params": {{}},
        "remember": null
    }}
    
    If the user tells you something to remember, set "remember" to:
    {{"key": "category.item", "value": "what to remember"}}
    
    Possible actions and their params:
    - "lights_on" : {{}}
    - "lights_off" : {{}}
    - "lights_movie_mode" : {{}}
    - "lights_study_mode" : {{}}
    - "lights_good_morning" : {{}}
    - "lights_party_mode" : {{}}
    - "lights_brightness" : {{"brightness": 0-100}}
    - "tv_on" : {{}}
    - "tv_off" : {{}}
    - "tv_volume_up" : {{"amount": 5}}
    - "tv_volume_down" : {{"amount": 5}}
    - "tv_mute" : {{}}
    - "tv_movie_mode" : {{}}
    - "spotify_play" : {{}}
    - "spotify_pause" : {{}}
    - "spotify_next" : {{}}
    - "spotify_previous" : {{}}
    - "spotify_volume" : {{"volume": 0-100}}
    - "spotify_play_song" : {{"song": "song name"}}
    - "spotify_play_playlist" : {{"playlist": "playlist name"}}
    - "spotify_current" : {{}}
    - "spotify_play_on_device" : {{"device": "device name"}}
    - "movie_mode" : {{}}
    - "study_mode" : {{}}
    - "good_morning" : {{}}
    - "get_weather" : {{}}
    - "get_time" : {{}}
    - "get_news" : {{}}
    - "calculate" : {{"expression": "math expression"}}
    - "get_joke" : {{}}
    - "set_timer" : {{"seconds": number}}
    - "get_battery" : {{}}
    - "set_volume" : {{"level": 0-100}}
    - "volume_up" : {{}}
    - "volume_down" : {{}}
    - "mute_mac" : {{}}
    - "open_app" : {{"app": "app name"}}
    - "lock_mac" : {{}}
    - "sleep_mac" : {{}}
    - "add_reminder" : {{"text": "reminder text", "time": "optional time"}}
    - "get_reminders" : {{}}
    - "none" : {{}}
    
    Always respond ONLY with the JSON object, nothing else."""

    # Add user message to history
    conversation_history.append({
        "role": "user",
        "content": command
    })

    # Keep history manageable
    if len(conversation_history) > MAX_HISTORY:
        conversation_history = conversation_history[-MAX_HISTORY:]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt}
        ] + conversation_history
    )

    raw = response.choices[0].message.content

    # Add assistant response to history
    conversation_history.append({
        "role": "assistant",
        "content": raw
    })

    try:
        clean = raw.replace("```json", "").replace("```", "").strip()
        result = json.loads(clean)
        return result
    except json.JSONDecodeError:
        return {
            "response": raw,
            "action": "none",
            "params": {},
            "remember": None
        }
    