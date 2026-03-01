import time
import threading
import subprocess
from datetime import datetime, timedelta
import json
import os

# Will be set from main.py
_speak = None
_handle_action = None

def init(speak_func, handle_action_func):
    """Initialize with speak and handle_action functions"""
    global _speak, _handle_action
    _speak = speak_func
    _handle_action = handle_action_func

# ─────────────────────────────────────────────
# TIME OF DAY LIGHT ADJUSTMENT
# ─────────────────────────────────────────────

last_light_period = None

def get_time_period():
    """Get current time period"""
    hour = datetime.now().hour
    if 5 <= hour < 9:
        return "dawn"
    elif 9 <= hour < 12:
        return "morning"
    elif 12 <= hour < 17:
        return "afternoon"
    elif 17 <= hour < 21:
        return "evening"
    elif 21 <= hour < 23:
        return "night"
    else:
        return "late_night"

def auto_adjust_lights():
    """Automatically adjust lights based on time of day"""
    global last_light_period
    period = get_time_period()

    if period == last_light_period:
        return

    last_light_period = period

    if period == "dawn":
        _handle_action("good_morning", {})
        _speak("Good morning sir. Adjusting lights for the day ahead.")
    elif period == "morning":
        _handle_action("study_mode", {})
    elif period == "afternoon":
        _handle_action("lights_colour", {"colour": "white"})
    elif period == "evening":
        _handle_action("lights_colour", {"colour": "orange"})
        _speak("Evening sir. Adjusting to a warmer light.")
    elif period == "night":
        _handle_action("lights_brightness", {"brightness": 30})
        _handle_action("lights_colour", {"colour": "indigo"})
        _speak("Dimming the lights for the evening sir.")
    elif period == "late_night":
        _handle_action("lights_brightness", {"brightness": 10})

# ─────────────────────────────────────────────
# DEADLINE REMINDERS
# ─────────────────────────────────────────────

last_deadline_check = None

def check_deadlines_auto():
    """Automatically remind about upcoming deadlines"""
    global last_deadline_check
    now = datetime.now()

    # Only check once per hour
    if last_deadline_check and (now - last_deadline_check).seconds < 3600:
        return
    last_deadline_check = now

    try:
        from core.engineering import load_deadlines
        deadlines = load_deadlines()
        for d in deadlines:
            try:
                due = datetime.strptime(d["due_date"], "%Y-%m-%d")
                days_left = (due - now).days
                hours_left = ((due - now).seconds // 3600)

                # Remind at 7 days, 3 days, 1 day and same day
                if days_left == 7:
                    _speak(f"Sir, a heads up — {d['title']} for {d['course']} is due in one week.")
                elif days_left == 3:
                    _speak(f"Sir, {d['title']} for {d['course']} is due in 3 days. I would suggest making progress soon.")
                elif days_left == 1:
                    _speak(f"Sir, urgent reminder — {d['title']} for {d['course']} is due tomorrow.")
                elif days_left == 0:
                    _speak(f"Sir, {d['title']} for {d['course']} is due today.")
            except:
                continue
    except:
        pass

# ─────────────────────────────────────────────
# STUDY MODE WHEN DEADLINE IS CLOSE
# ─────────────────────────────────────────────

study_mode_active = False

def auto_study_mode():
    """Activate study mode when a deadline is within 48 hours"""
    global study_mode_active
    try:
        from core.engineering import load_deadlines
        deadlines = load_deadlines()
        now = datetime.now()
        urgent = False

        for d in deadlines:
            try:
                due = datetime.strptime(d["due_date"], "%Y-%m-%d")
                days_left = (due - now).days
                if 0 <= days_left <= 2:
                    urgent = True
                    break
            except:
                continue

        if urgent and not study_mode_active:
            study_mode_active = True
            _handle_action("study_mode", {})
            _speak("Sir, you have a deadline approaching. Activating study mode to help you focus.")
        elif not urgent and study_mode_active:
            study_mode_active = False

    except:
        pass

# ─────────────────────────────────────────────
# MAC SLEEP DETECTION — AUTO LIGHTS OFF
# ─────────────────────────────────────────────

last_mac_active = True

def check_mac_sleep():
    """Detect if Mac has gone to sleep and turn off lights"""
    global last_mac_active
    try:
        result = subprocess.run(
            ['ioreg', '-n', 'IODisplayWrangler'],
            capture_output=True, text=True
        )
        # Only sleep if display power state is 0 (fully off)
        is_active = 'DevicePowerState" = 0' not in result.stdout
        
        if not is_active and last_mac_active:
            last_mac_active = False
            _handle_action("lights_off", {})
            print("Mac sleeping — lights turned off")
        elif is_active and not last_mac_active:
            last_mac_active = True
            print("Mac waking — restoring lights")
    except:
        pass

# ─────────────────────────────────────────────
# SCHEDULE LEARNING
# ─────────────────────────────────────────────

SCHEDULE_FILE = "jarvis_schedule.json"

def load_schedule():
    if os.path.exists(SCHEDULE_FILE):
        with open(SCHEDULE_FILE, 'r') as f:
            return json.load(f)
    return {"patterns": [], "suggestions_made": []}

def save_schedule(schedule):
    with open(SCHEDULE_FILE, 'w') as f:
        json.dump(schedule, f, indent=2)

def log_activity(action, hour=None):
    """Log user activity to learn patterns"""
    schedule = load_schedule()
    hour = hour or datetime.now().hour
    day = datetime.now().strftime("%A")
    pattern = {"action": action, "hour": hour, "day": day}
    schedule["patterns"].append(pattern)
    # Keep last 200 patterns
    schedule["patterns"] = schedule["patterns"][-200:]
    save_schedule(schedule)

def suggest_routine():
    """Suggest a routine based on learned patterns"""
    schedule = load_schedule()
    patterns = schedule.get("patterns", [])
    if len(patterns) < 20:
        return  # Not enough data yet

    now = datetime.now()
    hour = now.hour
    day = now.strftime("%A")

    # Find common actions at this hour on this day
    matching = [p for p in patterns
                if p["hour"] == hour and p["day"] == day]

    if len(matching) >= 3:
        # Find most common action
        action_counts = {}
        for p in matching:
            action_counts[p["action"]] = action_counts.get(p["action"], 0) + 1

        most_common = max(action_counts, key=action_counts.get)
        suggestion_key = f"{day}_{hour}_{most_common}"

        if suggestion_key not in schedule["suggestions_made"]:
            schedule["suggestions_made"].append(suggestion_key)
            save_schedule(schedule)
            _speak(f"Sir, you typically {most_common.replace('_', ' ')} around this time on {day}s. Shall I do that now?")

# ─────────────────────────────────────────────
# MAIN AUTONOMOUS LOOP
# ─────────────────────────────────────────────

def autonomous_loop():
    """Run all autonomous behaviors in background"""
    global check_interval
    print("Autonomous systems online")
    check_interval = 0

    # Wait 30 seconds before starting autonomous behavior
    time.sleep(30)

    while True:
        try:
            check_mac_sleep()

            if check_interval % 10 == 0:
                auto_adjust_lights()
                auto_study_mode()

            if check_interval % 60 == 0:
                check_deadlines_auto()
                suggest_routine()

            check_interval += 1
            time.sleep(30)

        except Exception as e:
            print(f"Autonomous loop error: {e}")
            time.sleep(30)

def start_autonomous(speak_func, handle_action_func):
    """Start autonomous systems in background thread"""
    init(speak_func, handle_action_func)
    thread = threading.Thread(target=autonomous_loop, daemon=True)
    thread.start()
    print("Autonomous systems started")
