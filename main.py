from ui.orb import set_orb_state, OrbWidget
import subprocess
import sys
import time
from devices import lights
from devices import tv as tv_device
from datetime import datetime
from core.skills import (get_weather, get_time, get_news, calculate, get_joke,
                    set_timer, get_battery, set_volume, volume_up,
                    volume_down, mute_mac, open_app, lock_mac, sleep_mac,
                    get_sports_scores, get_stock, wikipedia_search,
                    translate_text, random_fact, media_play_pause,
                    media_next, media_previous, send_imessage, get_directions)
from speech import speak, speak_wait, listen, wait_for_wake_word
from ai import ask_jarvis
from devices import spotify
from devices import arduino as arduino_device
from dashboard.app import run_dashboard, update_state
from core.memory import remember, add_reminder, get_reminders, clear_reminder
from ui.orb import launch_orb, set_orb_state
import threading
import json

# Start dashboard in background thread
dashboard_thread = threading.Thread(target=run_dashboard, daemon=True)
dashboard_thread.start()

# Launch orb
launch_orb()

# Connect to Arduino
arduino_connected = arduino_device.connect()

# Handle physical button presses
def on_button_press(btn):
    if btn == "BTN_MOVIE_MODE":
        speak("Movie mode activated sir.")
        handle_action("movie_mode", {})
    elif btn == "BTN_STUDY_MODE":
        speak("Study mode activated sir.")
        handle_action("study_mode", {})
    elif btn == "BTN_PARTY_MODE":
        speak("Party mode activated sir.")
        handle_action("lights_party_mode", {})
    elif btn == "BTN_GOOD_MORNING":
        speak("Good morning sir.")
        handle_action("good_morning", {})
    elif btn == "BTN_STOP":
        speak("Cancelling sir.")

if arduino_connected:
    arduino_device.set_button_callback(on_button_press)

def handle_action(action, params):
    """Route actions to the right device module"""
    update_state("last_action", action)
    try:
        # Spotify actions
        if action == "spotify_play":
            spotify.play()
            update_state("spotify", spotify.get_current_track())
        elif action == "spotify_pause":
            spotify.pause()
            update_state("spotify", "Paused")
        elif action == "spotify_next":
            spotify.next_track()
        elif action == "spotify_previous":
            spotify.previous_track()
        elif action == "spotify_volume":
            spotify.set_volume(params.get("volume", 50))
        elif action == "spotify_play_song":
            spotify.play_song(params.get("song", ""))
            update_state("spotify", spotify.get_current_track())
        elif action == "spotify_play_playlist":
            spotify.play_playlist(params.get("playlist", ""))
        elif action == "spotify_current":
            track = spotify.get_current_track()
            speak_wait(track)
            update_state("spotify", track)
        elif action == "spotify_play_on_device":
            spotify.play_on_device(params.get("device", ""))

        # Skills
        elif action == "get_weather":
            result = get_weather()
            speak_wait(result)
            update_state("last_action", result)
        elif action == "get_time":
            result = get_time()
            speak_wait(result)
        elif action == "get_news":
            result = get_news()
            speak_wait(result)
        elif action == "calculate":
            result = calculate(params.get("expression", ""))
            speak_wait(result)
        elif action == "get_joke":
            result = get_joke()
            speak_wait(result)
        elif action == "set_timer":
            seconds = params.get("seconds", 60)
            result = set_timer(seconds, speak)
            speak_wait(result)
        elif action == "get_battery":
            result = get_battery()
            speak_wait(result)
        elif action == "set_volume":
            result = set_volume(params.get("level", 50))
            speak_wait(result)
        elif action == "volume_up":
            result = volume_up()
            speak_wait(result)
        elif action == "volume_down":
            result = volume_down()
            speak_wait(result)
        elif action == "mute_mac":
            result = mute_mac()
            speak_wait(result)
        elif action == "open_app":
            result = open_app(params.get("app", ""))
            speak_wait(result)
        elif action == "lock_mac":
            result = lock_mac()
            speak_wait(result)
        elif action == "sleep_mac":
            result = sleep_mac()
            speak_wait(result)
        elif action == "get_sports":
            result = get_sports_scores(params.get("sport", "nhl"))
            speak_wait(result)
        elif action == "get_stock":
            result = get_stock(params.get("symbol", "AAPL"))
            speak_wait(result)
        elif action == "wikipedia":
            result = wikipedia_search(params.get("query", ""))
            speak_wait(result)
        elif action == "translate":
            result = translate_text(
                params.get("text", ""),
                params.get("language", "fr")
            )
            speak_wait(result)
        elif action == "random_fact":
            result = random_fact()
            speak_wait(result)
        elif action == "media_play_pause":
            result = media_play_pause()
            speak_wait(result)
        elif action == "media_next":
            result = media_next()
            speak_wait(result)
        elif action == "media_previous":
            result = media_previous()
            speak_wait(result)
        elif action == "send_imessage":
            result = send_imessage(
                params.get("contact", ""),
                params.get("message", "")
            )
            speak_wait(result)
        elif action == "get_directions":
            result = get_directions(params.get("destination", ""))
            speak_wait(result)

        # Memory actions
        elif action == "add_reminder":
            result = add_reminder(
                params.get("text", ""),
                params.get("time", None)
            )
            speak_wait(result)
        elif action == "get_reminders":
            result = get_reminders()
            speak_wait(result)

        # TV actions
        elif action == "tv_on":
            tv_device.turn_on()
            update_state("tv", "On")
            speak_wait("TV on sir.")
        elif action == "tv_off":
            tv_device.turn_off()
            update_state("tv", "Off")
            speak_wait("TV off sir.")
        elif action == "tv_volume_up":
            tv_device.volume_up(params.get("amount", 5))
            speak_wait("Volume up sir.")
        elif action == "tv_volume_down":
            tv_device.volume_down(params.get("amount", 5))
            speak_wait("Volume down sir.")
        elif action == "tv_mute":
            tv_device.mute()
            speak_wait("Muted sir.")
        elif action == "tv_movie_mode":
            tv_device.movie_mode()
            update_state("tv", "On")

        # Light actions
        elif action == "lights_on":
            lights.turn_on()
            update_state("lights", "On")
            speak_wait("Lights on sir.")
        elif action == "lights_off":
            lights.turn_off()
            update_state("lights", "Off")
            speak_wait("Lights off sir.")
        elif action == "lights_brightness":
            lights.set_brightness(params.get("brightness", 50))
        elif action == "lights_colour":
            result = lights.set_colour_by_name(params.get("colour", "white"))
            speak_wait(result)
            update_state("lights", params.get("colour", "white"))

        # Mode actions
        elif action == "movie_mode":
            lights.movie_mode()
            tv_device.turn_on()
            if arduino_connected:
                arduino_device.movie_mode()
            update_state("lights", "Movie Mode")
            update_state("tv", "On")
            speak_wait("Movie mode activated sir.")
        elif action == "study_mode":
            lights.study_mode()
            if arduino_connected:
                arduino_device.study_mode()
            update_state("lights", "Study Mode")
            speak_wait("Study mode activated sir.")
        elif action == "lights_party_mode":
            lights.party_mode()
            if arduino_connected:
                arduino_device.party_mode()
            update_state("lights", "Party Mode")
            speak_wait("Party mode activated sir.")
        elif action == "good_morning":
            lights.good_morning()
            if arduino_connected:
                arduino_device.good_morning()
            update_state("lights", "Morning Mode")
            speak_wait("Good morning sir.")
        elif action == "fan_on":
            if arduino_connected:
                arduino_device.fan_on()
            speak_wait("Fan on sir.")
        elif action == "fan_off":
            if arduino_connected:
                arduino_device.fan_off()
            speak_wait("Fan off sir.")

        elif action == "none":
            pass

    except Exception as e:
        print(f"Action error: {e}")
        speak_wait("I encountered an issue with that command sir.")

#bootup
def jarvis_main():
    """Main Jarvis loop — runs in background thread"""
    set_orb_state("idle")
    speak_wait("Good evening. J.A.R.V.I.S. online. All systems ready.")

    while True:
        if arduino_connected:
            arduino_device.status_idle()
        set_orb_state("idle")

        wait_for_wake_word()
        subprocess.run(['afplay', '/System/Library/Sounds/Tink.aiff'])

        if arduino_connected:
            arduino_device.status_listening()
        set_orb_state("listening")

        speak_wait("Yes?")

        for _ in range(3):
            command = listen()
            if not command:
                set_orb_state("idle")
                break

            print(f"Processing: {command}")
            update_state("last_command", command)

            if arduino_connected:
                arduino_device.status_processing()
            set_orb_state("processing")

            result = ask_jarvis(command)

            response = result.get("response", "")
            action = result.get("action", "none")
            params = result.get("params", {})
            memory_item = result.get("remember")

            print(f"Action: {action}")

            if arduino_connected:
                arduino_device.status_speaking()
            set_orb_state("speaking")

            if action != "none":
                speak_wait(response)
            else:
                speak_wait(response)

            set_orb_state("listening")
            handle_action(action, params)

            if memory_item:
                remember(memory_item.get("key", "notes"), memory_item.get("value", ""))

            if command == "stop" or action == "shutdown":
                speak_wait("Goodbye sir.")
                exit()

            if "?" not in response:
                break

            time.sleep(0.5)

# Start dashboard in background thread — only once
dashboard_thread = threading.Thread(target=run_dashboard, daemon=True)
dashboard_thread.start()

# Connect to Arduino
arduino_connected = arduino_device.connect()
if arduino_connected:
    arduino_device.set_button_callback(on_button_press)

# Start Jarvis main loop in background thread
jarvis_thread = threading.Thread(target=jarvis_main, daemon=True)
jarvis_thread.start()

# Launch orb on main thread — required by macOS
import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from ui.orb import OrbWidget, _state, set_orb_state as _set_state

qt_app = QApplication(sys.argv)
orb = OrbWidget()
orb.show()
qt_app.exec()