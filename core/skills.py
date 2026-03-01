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
    """Get Mac battery level and charging status"""
    try:
        result = subprocess.run(['pmset', '-g', 'batt'], capture_output=True, text=True)
        output = result.stdout
        
        # Get percentage
        import re
        match = re.search(r'(\d+)%', output)
        if not match:
            return "Battery level unavailable sir."
        pct = int(match.group(1))
        
        # Get charging status accurately
        if 'AC Power' in output:
            status = "charging"
        elif 'discharging' in output.lower():
            status = "not charging"
        else:
            status = "not charging"
            
        return f"Battery is at {pct} percent and {status} sir."
    except:
        return "Battery information unavailable sir."

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

import yfinance as yf
import wikipediaapi
import subprocess
import json

def get_sports_scores(team=None):
    """Get latest sports scores"""
    try:
        url = "https://site.api.espn.com/apis/site/v2/sports/hockey/nhl/scoreboard"
        response = requests.get(url)
        data = response.json()
        events = data.get("events", [])
        if not events:
            return "No games found today sir."
        result = "Here are today's scores. "
        for event in events[:3]:
            name = event.get("name", "")
            status = event["status"]["type"]["description"]
            comps = event.get("competitions", [{}])[0]
            competitors = comps.get("competitors", [])
            if len(competitors) == 2:
                team1 = competitors[0]["team"]["shortDisplayName"]
                score1 = competitors[0]["score"]
                team2 = competitors[1]["team"]["shortDisplayName"]
                score2 = competitors[1]["score"]
                result += f"{team1} {score1}, {team2} {score2} — {status}. "
        return result
    except Exception as e:
        return "I couldn't retrieve the scores sir."

def get_stock(symbol):
    """Get current stock price"""
    try:
        import yfinance as yf
        ticker = yf.Ticker(symbol.upper())
        info = ticker.fast_info
        price = round(info.last_price, 2)
        prev = round(info.previous_close, 2)
        change = round(price - prev, 2)
        direction = "up" if change > 0 else "down"
        return f"{symbol.upper()} is trading at {price} dollars, {direction} {abs(change)} from yesterday sir."
    except:
        return f"I couldn't retrieve the stock price for {symbol} sir."

def wikipedia_search(query):
    """Search Wikipedia for a topic"""
    try:
        import wikipediaapi
        wiki = wikipediaapi.Wikipedia(
            language='en',
            extract_format=wikipediaapi.ExtractFormat.WIKI,
            user_agent='JARVIS/1.0'
        )
        page = wiki.page(query)
        if page.exists():
            summary = page.summary[:500]
            sentences = summary.split('. ')
            return '. '.join(sentences[:2]) + '.'
        return f"I couldn't find anything on {query} sir."
    except:
        return f"I couldn't search Wikipedia right now sir."

def translate_text(text, target_language):
    """Translate text to another language"""
    try:
        from translate import Translator
        translator = Translator(to_lang=target_language)
        result = translator.translate(text)
        return f"The translation is: {result}"
    except:
        return "I couldn't translate that sir."


def random_fact():
    """Get a random interesting fact"""
    try:
        response = requests.get("https://uselessfacts.jsph.pl/random.json?language=en")
        data = response.json()
        return data.get("text", "I couldn't find a fact right now sir.")
    except:
        return "I couldn't retrieve a fact right now sir."

def media_play_pause():
    """Play or pause media on Mac"""
    subprocess.run(['osascript', '-e', 'tell application "System Events" to key code 49'])
    return "Done sir."

def media_next():
    """Skip to next track on Mac"""
    subprocess.run(['osascript', '-e', 'tell application "System Events" to key code 124 using command down'])
    return "Next track sir."

def media_previous():
    """Go to previous track on Mac"""
    subprocess.run(['osascript', '-e', 'tell application "System Events" to key code 123 using command down'])
    return "Previous track sir."

def send_imessage(contact, message):
    """Send an iMessage"""
    try:
        script = f'''
        tell application "Messages"
            set targetBuddy to "{contact}"
            set targetService to 1st account whose service type = iMessage
            send "{message}" to participant targetBuddy of targetService
        end tell
        '''
        subprocess.run(['osascript', '-e', script])
        return f"Message sent to {contact} sir."
    except:
        return f"I couldn't send the message sir."

def get_directions(destination):
    """Open directions in Apple Maps"""
    try:
        destination_encoded = destination.replace(' ', '+')
        subprocess.run(['open', f'maps://?daddr={destination_encoded}'])
        return f"Opening directions to {destination} sir."
    except:
        return "I couldn't open directions sir."

def set_wallpaper(image_path):
    """Set Mac wallpaper"""
    try:
        script = f'tell application "Finder" to set desktop picture to POSIX file "{image_path}"'
        subprocess.run(['osascript', '-e', script])
        return "Wallpaper updated sir."
    except:
        return "I couldn't change the wallpaper sir."
    
def get_weather_data():
    """Return raw weather data as dict for dashboard"""
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={WEATHER_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()
        return {
            "temp": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "description": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"]
        }
    except:
        return {}
