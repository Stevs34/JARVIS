import subprocess
from speech import speak, listen, wait_for_wake_word
from speech import speak, listen
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
            speak(track)
            update_state("spotify", track)
        elif action == "spotify_play_on_device":
            spotify.play_on_device(params.get("device", ""))

        # Placeholder actions for devices we'll connect at home
        elif action in ["lights_on", "lights_off", "lights_movie_mode",
                        "lights_study_mode", "lights_good_morning",
                        "lights_party_mode", "lights_brightness",
                        "tv_on", "tv_off", "tv_volume_up", "tv_volume_down",
                        "tv_mute", "tv_movie_mode", "movie_mode",
                        "study_mode", "good_morning"]:
            speak("That device isn't connected yet sir, but I'll handle it when it is.")

        elif action == "none":
            pass

    except Exception as e:
        print(f"Action error: {e}")
        speak("I encountered an issue with that command sir.")

# Boot up
speak("Good evening. J.A.R.V.I.S. online. All systems ready.")

while True:
    # Wait for wake word first
    wait_for_wake_word()
    
    # Wake word detected — play a subtle chime and listen
    subprocess.run(['afplay', '/System/Library/Sounds/Tink.aiff'])
    speak("Yes?")
    
    command = listen()
    if command:
        print(f"Processing: {command}")
        update_state("last_command", command)
        result = ask_jarvis(command)

        response = result.get("response", "")
        action = result.get("action", "none")
        params = result.get("params", {})

        print(f"Action: {action}")
        speak(response)
        handle_action(action, params)

        if command == "stop" or action == "shutdown":
            speak("Goodbye sir.")
            break
