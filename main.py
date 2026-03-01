import subprocess
import time
from skills import (get_weather, get_time, get_news, calculate, get_joke,
                    set_timer, get_battery, set_volume, volume_up, 
                    volume_down, mute_mac, open_app, lock_mac, sleep_mac)
from speech import speak, speak_wait, listen, wait_for_wake_word
from ai import ask_jarvis
from devices import spotify
from dashboard.app import run_dashboard, update_state
import threading
import json

# Start dashboard in background thread
dashboard_thread = threading.Thread(target=run_dashboard, daemon=True)
dashboard_thread.start()

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

        # Placeholder actions for devices we'll connect at home
        elif action in ["lights_on", "lights_off", "lights_movie_mode",
                        "lights_study_mode", "lights_good_morning",
                        "lights_party_mode", "lights_brightness",
                        "tv_on", "tv_off", "tv_volume_up", "tv_volume_down",
                        "tv_mute", "tv_movie_mode", "movie_mode",
                        "study_mode", "good_morning"]:
            speak_wait("That device isn't connected yet sir, but I'll handle it when it is.")

        elif action == "none":
            pass

    except Exception as e:
        print(f"Action error: {e}")
        speak_wait("I encountered an issue with that command sir.")

# Boot up
speak_wait("Good evening. J.A.R.V.I.S. online. All systems ready.")

while True:
    # Wait for wake word
    wait_for_wake_word()
    subprocess.run(['afplay', '/System/Library/Sounds/Tink.aiff'])
    speak_wait("Yes?")

    # Allow up to 3 back and forth exchanges without wake word
    for _ in range(3):
        command = listen()
        if not command:
            break

        print(f"Processing: {command}")
        update_state("last_command", command)
        result = ask_jarvis(command)

        response = result.get("response", "")
        action = result.get("action", "none")
        params = result.get("params", {})

        print(f"Action: {action}")

        # If there's a skill action, wait for response to finish first
        if action != "none":
            speak_wait(response)
        else:
            speak_wait(response)

        handle_action(action, params)

        if command == "stop" or action == "shutdown":
            speak_wait("Goodbye sir.")
            exit()

        # If Jarvis asked a question keep listening
        if "?" not in response:
            break

        time.sleep(0.5)
        