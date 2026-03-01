import tinytuya
import os
import colorsys
import threading
from dotenv import load_dotenv

load_dotenv()

LIGHT_DEVICE_ID = os.getenv("TUYA_LIGHT_DEVICE_ID")
LIGHT_LOCAL_KEY = os.getenv("TUYA_LIGHT_LOCAL_KEY")
LIGHT_IP = os.getenv("TUYA_LIGHT_IP")

def connect_light():
    device = tinytuya.BulbDevice(
        dev_id=LIGHT_DEVICE_ID,
        address=LIGHT_IP,
        local_key=LIGHT_LOCAL_KEY,
        version=3.3
    )
    return device

def rgb_to_payload(r, g, b):
    h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
    h = int(h * 360)
    s = int(s * 1000)
    v = int(v * 1000)
    return f"{h:04x}{s:04x}{v:04x}"

def set_colour(r, g, b):
    d = connect_light()
    payload = rgb_to_payload(r, g, b)
    d.set_value(21, 'colour')
    d.set_value(24, payload)

def fade_to_colour(r2, g2, b2, steps=10):
    import time
    try:
        d = connect_light()
        status = d.status()
        current = status.get('dps', {}).get('24', '000003e803e8')
        r1 = int(current[0:4], 16) / 360 * 255
        g1 = int(current[4:8], 16) / 1000 * 255
        b1 = int(current[8:12], 16) / 1000 * 255
        for i in range(1, steps + 1):
            t = i / steps
            r = int(r1 + (r2 - r1) * t)
            g = int(g1 + (g2 - g1) * t)
            b = int(b1 + (b2 - b1) * t)
            payload = rgb_to_payload(r, g, b)
            d.set_value(21, 'colour')
            d.set_value(24, payload)
            time.sleep(0.05)
    except:
        set_colour(r2, g2, b2)

def turn_on():
    d = connect_light()
    d.set_value(20, True)

def turn_off():
    d = connect_light()
    d.set_value(20, False)

def set_brightness(brightness):
    d = connect_light()
    value = int(brightness * 10)
    d.set_value(22, value)

def movie_mode():
    threading.Thread(target=fade_to_colour, args=(20, 0, 40), daemon=True).start()

def study_mode():
    d = connect_light()
    d.set_value(21, 'white')
    d.set_value(22, 1000)

def good_morning():
    threading.Thread(target=fade_to_colour, args=(255, 147, 41), daemon=True).start()

def party_mode():
    threading.Thread(target=fade_to_colour, args=(255, 0, 128), daemon=True).start()

def set_colour_by_name(colour_name):
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
        threading.Thread(target=fade_to_colour, args=(r, g, b), daemon=True).start()
        return f"Lights fading to {colour_name} sir."
    return f"I don't know the colour {colour_name} sir."
