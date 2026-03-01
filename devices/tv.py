import pyvizio
import os
from dotenv import load_dotenv

load_dotenv()

VIZIO_IP = os.getenv("VIZIO_IP")
VIZIO_AUTH_TOKEN = os.getenv("VIZIO_AUTH_TOKEN")

def get_tv():
    """Connect to your Vizio TV"""
    return pyvizio.Vizio(
        device_id="jarvis",
        ip=VIZIO_IP,
        name="Jarvis",
        auth_token=VIZIO_AUTH_TOKEN,
        device_type=pyvizio.DEVICE_CLASS_TV
    )

def turn_on():
    tv = get_tv()
    tv.pow_on()
    print("TV on")

def turn_off():
    tv = get_tv()
    tv.pow_off()
    print("TV off")

def volume_up(amount=5):
    tv = get_tv()
    for _ in range(amount):
        tv.vol_up()
    print(f"Volume up {amount}")

def volume_down(amount=5):
    tv = get_tv()
    for _ in range(amount):
        tv.vol_down()
    print(f"Volume down {amount}")

def mute():
    tv = get_tv()
    tv.mute_toggle()
    print("Mute toggled")

def set_input(input_name):
    """Switch input e.g. HDMI-1, HDMI-2"""
    tv = get_tv()
    tv.set_input(input_name)
    print(f"Input set to {input_name}")

def get_inputs():
    """Get list of available inputs"""
    tv = get_tv()
    return tv.get_inputs_list()

def movie_mode():
    """Turn on TV"""
    turn_on()
    print("TV movie mode activated")

def get_power_state():
    tv = get_tv()
    return tv.get_power_state()
