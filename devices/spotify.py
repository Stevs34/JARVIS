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

def play():
    """Resume playback"""
    sp.start_playback()
    print("Spotify playing")

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
    