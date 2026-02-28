import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

load_dotenv()

scope = "user-modify-playback-state user-read-playback-state user-read-currently-playing"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
    scope=scope
))

DEVICES = {
    "kitchen": "b40e70ad-50d8-4ee3-9880-07828cac9ecf_amzn_2",
    "garage": "c7830080-383a-4738-8d37-28ea2479d04e_amzn_1",
    "everywhere": "47dbdda6-e490-4f54-9f45-1aa7ed7dbc65_amzn_4",
    "bevs room": "248ed713-f484-434c-a14f-6ddc345b8423_amzn_1",
    "mollys room": "b40e70ad-50d8-4ee3-9880-07828cac9ecf_amzn_1",
    "mom and dads room": "47dbdda6-e490-4f54-9f45-1aa7ed7dbc65_amzn_1",
    "bevs echo": "77fb0c75-7876-43f2-92a1-ad754d8ea738_amzn_1"
}

def play():
    """Resume playback — falls back to first available device"""
    try:
        sp.start_playback()
        print("Spotify playing")
    except Exception:
        devices = sp.devices()
        if devices["devices"]:
            device_id = devices["devices"][0]["id"]
            sp.transfer_playback(device_id=device_id, force_play=True)
            print(f"Transferred to {devices['devices'][0]['name']}")
        else:
            print("No devices available")

def play_on_device(device_name):
    """Play Spotify on a specific device by name"""
    device_name_lower = device_name.lower()

    # Check static devices first
    if device_name_lower in DEVICES:
        sp.transfer_playback(device_id=DEVICES[device_name_lower], force_play=True)
        print(f"Playing on {device_name}")
        return

    # Search live devices for Apple devices or anything not in static list
    devices = sp.devices()
    for d in devices["devices"]:
        if device_name_lower in d["name"].lower():
            sp.transfer_playback(device_id=d["id"], force_play=True)
            print(f"Playing on {d['name']}")
            return

    print(f"Could not find device: {device_name}")
    print("Available devices:")
    for d in devices["devices"]:
        print(f"  - {d['name']}")

def pause():
    """Pause playback"""
    sp.pause_playback()
    print("Spotify paused")

def next_track():
    """Skip to next track"""
    sp.next_track()
    print("Next track")

def previous_track():
    """Go to previous track"""
    sp.previous_track()
    print("Previous track")

def set_volume(volume):
    """Set volume 0-100"""
    sp.volume(volume)
    print(f"Spotify volume set to {volume}%")

def play_playlist(playlist_name):
    """Search for a playlist and play it"""
    results = sp.search(q=playlist_name, type="playlist", limit=1)
    if results["playlists"]["items"]:
        uri = results["playlists"]["items"][0]["uri"]
        sp.start_playback(context_uri=uri)
        print(f"Playing playlist: {playlist_name}")
    else:
        print(f"Playlist not found: {playlist_name}")

def play_song(song_name):
    """Search for a song and play it"""
    results = sp.search(q=song_name, type="track", limit=1)
    if results["tracks"]["items"]:
        uri = results["tracks"]["items"][0]["uri"]
        sp.start_playback(uris=[uri])
        print(f"Playing: {song_name}")
    else:
        print(f"Song not found: {song_name}")

def get_current_track():
    """Get the currently playing track"""
    current = sp.current_playback()
    if current and current["is_playing"]:
        track = current["item"]["name"]
        artist = current["item"]["artists"][0]["name"]
        return f"{track} by {artist}"
    return "Nothing playing"

if __name__ == "__main__":
    print(get_current_track())