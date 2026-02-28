import tinytuya
import os
from dotenv import load_dotenv

load_dotenv()

# We'll fill in your device ID and IP when you get home
LIGHT_DEVICE_ID = os.getenv("TUYA_LIGHT_DEVICE_ID")
LIGHT_LOCAL_KEY = os.getenv("TUYA_LIGHT_LOCAL_KEY")
LIGHT_IP = os.getenv("TUYA_LIGHT_IP")

def connect_light():
    """Connect to your Smart Life light"""
    device = tinytuya.BulbDevice(
        dev_id=LIGHT_DEVICE_ID,
        address=LIGHT_IP,
        local_key=LIGHT_LOCAL_KEY,
        version=3.3
    )
    return device

def turn_on():
    d = connect_light()
    d.turn_on()
    print("Lights on")

def turn_off():
    d = connect_light()
    d.turn_off()
    print("Lights off")

def set_brightness(brightness):
    """Set brightness 0-100"""
    d = connect_light()
    d.set_brightness_percentage(brightness)
    print(f"Brightness set to {brightness}%")

def set_colour(r, g, b):
    """Set colour using RGB values 0-255"""
    d = connect_light()
    d.set_colour(r, g, b)
    print(f"Colour set to RGB({r}, {g}, {b})")

def movie_mode():
    """Dim lights to red/blue for movie watching"""
    d = connect_light()
    d.turn_on()
    d.set_brightness_percentage(20)
    d.set_colour(20, 0, 40)
    print("Movie mode activated")

def study_mode():
    """Bright white light for studying"""
    d = connect_light()
    d.turn_on()
    d.set_brightness_percentage(100)
    d.set_colour(255, 255, 255)
    print("Study mode activated")

def good_morning():
    """Soft warm light to wake up"""
    d = connect_light()
    d.turn_on()
    d.set_brightness_percentage(60)
    d.set_colour(255, 147, 41)
    print("Good morning mode activated")

def party_mode():
    """Bright colours for party vibes"""
    d = connect_light()
    d.turn_on()
    d.set_brightness_percentage(100)
    d.set_colour(255, 0, 128)
    print("Party mode activated")
