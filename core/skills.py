import requests
import os
import datetime
import subprocess
import threading
from dotenv import load_dotenv

load_dotenv()

WEATHER_KEY = os.getenv("OPENWEATHER_API_KEY")
CITY = os.getenv("CITY", "Fredericton")

def get_weather():
    """Get current weather"""
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={WEATHER_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()
        temp = round(data["main"]["temp"])
        feels_like = round(data["main"]["feels_like"])
        description = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]
        return f"Currently {temp} degrees celsius in {CITY}, feels like {feels_like}. {description.capitalize()} with {humidity}% humidity."
    except Exception as e:
        return "I couldn't retrieve the weather at this time sir."

def get_time():
    """Get current time"""
    now = datetime.datetime.now()
    return f"It's {now.strftime('%I:%M %p')} on {now.strftime('%A, %B %d %Y')}."

def get_news():
    """Get top news headlines"""
    try:
        url = f"https://gnews.io/api/v4/top-headlines?lang=en&country=ca&max=3&apikey={os.getenv('GNEWS_API_KEY')}"
        response = requests.get(url)
        data = response.json()
        headlines = [a["title"] for a in data["articles"]]
        result = "Here are the top headlines. "
        for i, h in enumerate(headlines, 1):
            result += f"{i}. {h}. "
        return result
    except:
        return "I couldn't retrieve the news at this time sir."

def calculate(expression):
    """Safely evaluate a math expression"""
    try:
        allowed = set("0123456789+-*/()., ")
        if all(c in allowed for c in expression):
            result = eval(expression)
            return f"The answer is {result}."
        return "I couldn't calculate that sir."
    except:
        return "I couldn't calculate that sir."

def get_joke():
    """Get a random joke"""
    try:
        response = requests.get("https://official-joke-api.appspot.com/random_joke")
        data = response.json()
        return f"{data['setup']} ... {data['punchline']}"
    except:
        return "I couldn't think of a joke right now sir."

def set_timer(seconds, speak_func):
    """Set a timer for a given number of seconds"""
    def timer_thread():
        threading.Event().wait(seconds)
        speak_func(f"Sir, your {seconds} second timer is up.")
        subprocess.run(['afplay', '/System/Library/Sounds/Glass.aiff'])
    t = threading.Thread(target=timer_thread, daemon=True)
    t.start()
    minutes = seconds // 60
    secs = seconds % 60
    if minutes > 0:
        return f"Timer set for {minutes} minutes and {secs} seconds sir."
    return f"Timer set for {seconds} seconds sir."

def get_battery():
    """Get MacBook battery level"""
    try:
        result = subprocess.run(
            ['pmset', '-g', 'batt'],
            capture_output=True, text=True
        )
        output = result.stdout
        for line in output.split('\n'):
            if '%' in line:
                percent = line.split('\t')[1].split('%')[0].strip().split(';')[0]
                charging = 'charging' in line.lower()
                status = "and charging" if charging else "and not charging"
                return f"Battery is at {percent} percent {status} sir."
        return "I couldn't read the battery level sir."
    except:
        return "I couldn't read the battery level sir."

def set_volume(level):
    """Set Mac system volume 0-100"""
    try:
        subprocess.run(['osascript', '-e', f'set volume output volume {level}'])
        return f"Volume set to {level} percent sir."
    except:
        return "I couldn't set the volume sir."

def volume_up():
    """Increase Mac volume by 10"""
    try:
        script = 'set volume output volume (output volume of (get volume settings) + 10)'
        subprocess.run(['osascript', '-e', script])
        return "Volume increased sir."
    except:
        return "I couldn't increase the volume sir."

def volume_down():
    """Decrease Mac volume by 10"""
    try:
        script = 'set volume output volume (output volume of (get volume settings) - 10)'
        subprocess.run(['osascript', '-e', script])
        return "Volume decreased sir."
    except:
        return "I couldn't decrease the volume sir."

def mute_mac():
    """Mute Mac system volume"""
    try:
        subprocess.run(['osascript', '-e', 'set volume output muted true'])
        return "Muted sir."
    except:
        return "I couldn't mute the volume sir."

def open_app(app_name):
    """Open a Mac application by name"""
    try:
        subprocess.Popen(['open', '-a', app_name])
        return f"Opening {app_name} sir."
    except:
        return f"I couldn't find {app_name} sir."

def lock_mac():
    """Lock the Mac screen"""
    try:
        subprocess.run([
            'osascript', '-e',
            'tell application "System Events" to keystroke "q" using {command down, control down}'
        ])
        return "Locking your screen sir."
    except:
        return "I couldn't lock the screen sir."

def sleep_mac():
    """Put Mac to sleep"""
    try:
        subprocess.run(['pmset', 'sleepnow'])
        return "Going to sleep sir."
    except:
        return "I couldn't sleep the Mac sir."
