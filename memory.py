import json
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

MEMORY_FILE = "jarvis_memory.json"

def load_memory():
    """Load memory from file"""
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, 'r') as f:
            return json.load(f)
    return {
        "user": {
            "name": "Cole",
            "degree": "Mechanical Engineering",
            "year": "2nd year",
            "university": "University of New Brunswick",
            "city": "Fredericton"
        },
        "preferences": {},
        "reminders": [],
        "notes": [],
        "conversation_count": 0,
        "last_seen": None
    }

def save_memory(memory):
    """Save memory to file"""
    with open(MEMORY_FILE, 'w') as f:
        json.dump(memory, f, indent=2)

def get_memory_context():
    """Return memory as a string for the AI prompt"""
    memory = load_memory()
    memory["conversation_count"] += 1
    memory["last_seen"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    save_memory(memory)

    context = f"""
    User profile:
    - Name: {memory['user'].get('name', 'Cole')}
    - Degree: {memory['user'].get('degree', 'Mechanical Engineering')}
    - Year: {memory['user'].get('year', '2nd year')}
    - University: {memory['user'].get('university', 'University of New Brunswick')}
    - City: {memory['user'].get('city', 'Fredericton')}
    - Conversation count: {memory['conversation_count']}
    - Last seen: {memory['last_seen']}

    Preferences: {json.dumps(memory.get('preferences', {}))}
    
    Active reminders: {json.dumps(memory.get('reminders', []))}
    
    Notes: {json.dumps(memory.get('notes', []))}
    """
    return context

def remember(key, value):
    """Store something in memory"""
    memory = load_memory()
    if "." in key:
        section, item = key.split(".", 1)
        if section not in memory:
            memory[section] = {}
        memory[section][item] = value
    else:
        memory["notes"].append({
            "note": value,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
        })
    save_memory(memory)
    return f"I'll remember that sir."

def add_reminder(text, time_str=None):
    """Add a reminder"""
    memory = load_memory()
    reminder = {
        "text": text,
        "time": time_str,
        "created": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    memory["reminders"].append(reminder)
    save_memory(memory)
    return f"Reminder set: {text}"

def get_reminders():
    """Get all reminders"""
    memory = load_memory()
    reminders = memory.get("reminders", [])
    if not reminders:
        return "You have no reminders sir."
    result = "Your reminders: "
    for i, r in enumerate(reminders, 1):
        result += f"{i}. {r['text']}. "
    return result

def clear_reminder(index):
    """Remove a reminder by index"""
    memory = load_memory()
    if 0 < index <= len(memory["reminders"]):
        removed = memory["reminders"].pop(index - 1)
        save_memory(memory)
        return f"Removed reminder: {removed['text']}"
    return "I couldn't find that reminder sir."
