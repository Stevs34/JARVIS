import requests
import os
import datetime
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