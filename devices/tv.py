import pyvizio
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

VIZIO_IP = os.getenv("VIZIO_IP")
VIZIO_AUTH_TOKEN = os.getenv("VIZIO_AUTH_TOKEN")
VIZIO_PORT = 7345

def get_tv():
    """Connect to your Vizio TV"""
    return pyvizio.Vizio(
        device_id="jarvis",
        ip=VIZIO_IP,
        name="Jarvis",
        auth_token=VIZIO_AUTH_TOKEN,
        device_type=pyvizio.DeviceType.TV
    )

def turn_on():
    tv = get_tv()
    asyncio.run(tv.pow_on())
    print("TV on")

def turn_off():
    tv = get_tv()
    asyncio.run(tv.pow_off())
    print("TV off")

def volume_up(amount=5):
    tv = get_tv()
    asyncio.run(tv.vol_up(amount))
    print(f"Volume up {amount}")

def volume_down(amount=5):
    tv = get_tv()
    asyncio.run(tv.vol_down(amount))
    print(f"Volume down {amount}")

def mute():
    tv = get_tv()
    asyncio.run(tv.mute_toggle())
    print("Mute toggled")

def set_input(input_name):
    """Switch input e.g. HDMI-1, HDMI-2"""
    tv = get_tv()
    asyncio.run(tv.set_input(input_name))
    print(f"Input set to {input_name}")

def movie_mode():
    """Turn on TV and set to HDMI-1"""
    turn_on()
    set_input("HDMI-1")
    print("TV movie mode activated")

async def pair_tv():
    """Run this once at home to get your auth token"""
    tv = pyvizio.Vizio(
        device_id="jarvis",
        ip=VIZIO_IP,
        name="Jarvis",
        auth_token="",
        device_type=pyvizio.DeviceType.TV
    )
    await tv.start_pair()
    pin = input("Enter the PIN shown on your TV: ")
    result = await tv.finish_pair(pin)
    print(f"Your auth token is: {result.auth_token}")
    print("Add this to your .env file as VIZIO_AUTH_TOKEN")

if __name__ == "__main__":
    asyncio.run(pair_tv())
    