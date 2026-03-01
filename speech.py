import speech_recognition as sr
import subprocess
import pvporcupine
import pyaudio
import struct
import os
import threading
import tempfile
import queue
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv

load_dotenv()

PICOVOICE_KEY = os.getenv("PICOVOICE_ACCESS_KEY")
ELEVENLABS_KEY = os.getenv("ELEVENLABS_API_KEY")

# Initialize ElevenLabs client
el_client = ElevenLabs(api_key=ELEVENLABS_KEY)

# Initialize recognizer once globally with optimized settings
recognizer = sr.Recognizer()
recognizer.pause_threshold = 0.8        # Faster cutoff after speech ends
recognizer.phrase_threshold = 0.2       # Start detecting speech faster
recognizer.non_speaking_duration = 0.5  # Less wait after speech ends
recognizer.energy_threshold = 250       # More sensitive microphone
recognizer.dynamic_energy_threshold = False

# Pre-warm microphone on startup
_mic = None
def _init_mic():
    global _mic
    try:
        _mic = sr.Microphone()
        with _mic as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.3)
        print("Microphone initialized")
    except:
        pass

threading.Thread(target=_init_mic, daemon=True).start()

# Audio playback queue to prevent overlap
_audio_queue = queue.Queue()
_playback_lock = threading.Lock()

def play_audio(audio_bytes):
    """Play audio bytes using afplay"""
    with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
        f.write(audio_bytes)
        temp_path = f.name
    try:
        subprocess.run(['afplay', temp_path], check=True)
    except:
        pass
    finally:
        try:
            os.unlink(temp_path)
        except:
            pass

def _generate_and_play(text):
    """Generate ElevenLabs audio and play it"""
    try:
        audio = el_client.text_to_speech.convert(
            text=text,
            voice_id="onwK4e9ZLuTAKqWW03F9",
            model_id="eleven_turbo_v2_5",  # Faster model
            output_format="mp3_44100_96",   # Slightly compressed for speed
            voice_settings={
                "stability": 0.45,          # More natural variation
                "similarity_boost": 0.80,
                "style": 0.15,              # Subtle expressiveness
                "use_speaker_boost": True
            }
        )
        audio_bytes = b"".join(chunk for chunk in audio)
        play_audio(audio_bytes)
    except Exception as e:
        print(f"ElevenLabs error: {e}")
        subprocess.run(['say', '-v', 'Daniel', '-r', '185', text])

def speak(text):
    """Non-blocking speak"""
    if not text or not text.strip():
        return
    print(f"Jarvis: {text}")
    threading.Thread(target=_generate_and_play, args=(text,), daemon=True).start()

def speak_wait(text):
    """Blocking speak — waits until finished"""
    if not text or not text.strip():
        return
    print(f"Jarvis: {text}")
    with _playback_lock:
        _generate_and_play(text)

def wait_for_wake_word():
    """Listen for Jarvis wake word — optimized"""
    porcupine = pvporcupine.create(
        access_key=PICOVOICE_KEY,
        keywords=["jarvis"],
        sensitivities=[0.6]  # Slightly more sensitive
    )
    pa = pyaudio.PyAudio()
    stream = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length
    )
    print("Waiting for wake word 'Jarvis'...")
    try:
        while True:
            pcm = stream.read(porcupine.frame_length, exception_on_overflow=False)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
            result = porcupine.process(pcm)
            if result >= 0:
                print("Wake word detected!")
                return
    finally:
        stream.stop_stream()
        stream.close()
        pa.terminate()
        porcupine.delete()

def listen():
    """Listen for a voice command — optimized"""
    global _mic
    try:
        mic = _mic or sr.Microphone()
        with mic as source:
            print("Listening...")
            try:
                audio = recognizer.listen(
                    source,
                    timeout=6,
                    phrase_time_limit=12
                )
                command = recognizer.recognize_google(
                    audio,
                    language="en-CA",  # Canadian English for better accuracy
                    show_all=False
                )
                print(f"You said: {command}")
                return command.lower()
            except sr.WaitTimeoutError:
                return None
            except sr.UnknownValueError:
                return None
            except sr.RequestError:
                speak("Speech service unavailable sir.")
                return None
    except Exception as e:
        print(f"Listen error: {e}")
        return None
    