import tinytuya
import os
import colorsys
from dotenv import load_dotenv

load_dotenv()

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

def rgb_to_payload(r, g, b):
    """Convert RGB to Tuya HSV hex string"""
    h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
    h = int(h * 360)
    s = int(s * 1000)
    v = int(v * 1000)
    return f"{h:04x}{s:04x}{v:04x}"

def set_colour(r, g, b):
    """Set colour using RGB values 0-255"""
    d = connect_light()
    payload = rgb_to_payload(r, g, b)
    d.set_value(21, 'colour')
    d.set_value(24, payload)
    print(f"Colour set to RGB({r}, {g}, {b})")

def turn_on():
    d = connect_light()
    d.set_value(20, True)
    print("Lights on")

def turn_off():
    d = connect_light()
    d.set_value(20, False)
    print("Lights off")

def set_brightness(brightness):
    """Set brightness 0-100"""
    d = connect_light()
    value = int(brightness * 10)
    d.set_value(22, value)
    print(f"Brightness set to {brightness}%")

def movie_mode():
    """Dim purple for movie watching"""
    set_colour(20, 0, 40)
    print("Movie mode activated")

def study_mode():
    """Bright white for studying"""
    d = connect_light()
    d.set_value(21, 'white')
    d.set_value(22, 1000)
    print("Study mode activated")

def good_morning():
    """Soft warm orange"""
    set_colour(255, 147, 41)
    print("Good morning mode activated")

def party_mode():
    """Bright pink for party"""
    set_colour(255, 0, 128)
    print("Party mode activated")

def set_colour_by_name(colour_name):
    """Set light colour by name"""
    colours = {
        "red": (255, 0, 0),
        "green": (0, 255, 0),
        "blue": (0, 0, 255),
        "purple": (128, 0, 128),
        "pink": (255, 0, 128),
        "orange": (255, 165, 0),
        "yellow": (255, 255, 0),
        "white": (255, 255, 255),
        "teal": (0, 128, 128),
        "cyan": (0, 255, 255),
        "magenta": (255, 0, 255),
        "lime": (0, 255, 128),
        "indigo": (75, 0, 130),
        "violet": (238, 130, 238),
        "gold": (255, 215, 0),
        "coral": (255, 127, 80),
        "turquoise": (64, 224, 208),
        "crimson": (220, 20, 60),
        "lavender": (230, 230, 250),
        "mint": (152, 255, 152)
    }
    colour = colours.get(colour_name.lower())
    if colour:
        r, g, b = colour
        set_colour(r, g, b)
        return f"Lights set to {colour_name} sir."
    return f"I don't know the colour {colour_name} sir."
