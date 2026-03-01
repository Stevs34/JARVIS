from openai import OpenAI
from dotenv import load_dotenv
from core.memory import get_memory_context
import os
import json

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

conversation_history = []
MAX_HISTORY = 6

def ask_jarvis(command):
    """Send a command to ChatGPT and get a response"""
    global conversation_history

    memory_context = get_memory_context()

    actions = """
    - "lights_on" : {}
    - "lights_off" : {}
    - "lights_movie_mode" : {}
    - "lights_study_mode" : {}
    - "lights_good_morning" : {}
    - "lights_party_mode" : {}
    - "lights_brightness" : {"brightness": 0-100}
    - "lights_colour" : {"colour": "colour name e.g. red, blue, purple"}
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
    - "get_weather" : {}
    - "get_time" : {}
    - "get_news" : {}
    - "calculate" : {"expression": "math expression"}
    - "get_joke" : {}
    - "set_timer" : {"seconds": number}
    - "get_battery" : {}
    - "set_volume" : {"level": 0-100}
    - "volume_up" : {}
    - "volume_down" : {}
    - "mute_mac" : {}
    - "open_app" : {"app": "app name"}
    - "lock_mac" : {}
    - "sleep_mac" : {}
    - "add_reminder" : {"text": "reminder text", "time": "optional time"}
    - "get_reminders" : {}
    - "get_sports" : {"sport": "nhl/nba/nfl"}
    - "get_stock" : {"symbol": "ticker symbol e.g. AAPL"}
    - "wikipedia" : {"query": "search term"}
    - "translate" : {"text": "text to translate", "language": "target language"}
    - "random_fact" : {}
    - "media_play_pause" : {}
    - "media_next" : {}
    - "media_previous" : {}
    - "send_imessage" : {"contact": "name or number", "message": "message text"}
    - "get_directions" : {"destination": "address or place"}
    - "none" : {}
    """

    system_prompt = (
        "You are JARVIS, an AI assistant from Iron Man.\n"
        "You are helpful, intelligent, slightly formal but with wit and personality.\n"
        "You address the user as 'sir' occasionally but not every sentence.\n"
        "Keep responses SHORT — 1 sentence maximum unless asked for more detail.\n"
        "You have been with this user for a while and know them well.\n\n"
        f"Here is what you know about the user:\n{memory_context}\n\n"
        "You control a smart home system. When the user gives a command,\n"
        "respond with a JSON object in this exact format:\n"
        '{"response": "what Jarvis says out loud", "action": "the action to take", "params": {}, "remember": null}\n\n'
        "If the user tells you something to remember, set remember to:\n"
        '{"key": "category.item", "value": "what to remember"}\n\n'
        "Possible actions and their params:\n"
        + actions +
        "\nAlways respond ONLY with the JSON object, nothing else.\n"
        "Keep the response field to 1 short sentence for speed.\n"
        "For actions that fetch data like get_stock, get_weather, get_time, wikipedia, get_sports, random_fact — set response to an empty string '' since the skill will speak the result directly."
    )

    conversation_history.append({
        "role": "user",
        "content": command
    })

    if len(conversation_history) > MAX_HISTORY:
        conversation_history = conversation_history[-MAX_HISTORY:]

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt}
            ] + conversation_history,
            max_tokens=150,
            temperature=0.7
        )

        raw = response.choices[0].message.content

        conversation_history.append({
            "role": "assistant",
            "content": raw
        })

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
    except Exception as e:
        print(f"AI error: {e}")
        return {
            "response": "I encountered an issue sir.",
            "action": "none",
            "params": {},
            "remember": None
        }
