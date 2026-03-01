import speech_recognition as sr
import subprocess
import pvporcupine
import pyaudio
import struct
import os
import threading
import tempfile
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv

load_dotenv()

PICOVOICE_KEY = os.getenv("PICOVOICE_ACCESS_KEY")
ELEVENLABS_KEY = os.getenv("ELEVENLABS_API_KEY")

# Initialize ElevenLabs client
el_client = ElevenLabs(api_key=ELEVENLABS_KEY)

# Initialize recognizer once globally
recognizer = sr.Recognizer()
recognizer.pause_threshold = 1.5
recognizer.phrase_threshold = 0.3
recognizer.non_speaking_duration = 0.8
recognizer.energy_threshold = 300
recognizer.dynamic_energy_threshold = False

def play_audio(audio):
    """Play audio bytes using Mac's built in afplay"""
    audio_bytes = b"".join(chunk for chunk in audio)
    with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
        f.write(audio_bytes)
        temp_path = f.name
    subprocess.run(['afplay', temp_path])
    os.unlink(temp_path)

def speak(text):
    """Jarvis speaks using ElevenLabs — non blocking"""
    print(f"Jarvis: {text}")
    def _speak():
        try:
            audio = el_client.text_to_speech.convert(
                text=text,
                voice_id="onwK4e9ZLuTAKqWW03F9",
                model_id="eleven_turbo_v2",
                output_format="mp3_44100_128"
            )
            play_audio(audio)
        except Exception as e:
            print(f"ElevenLabs error: {e}")
            subprocess.run(['say', '-v', 'Daniel', text])
    threading.Thread(target=_speak, daemon=True).start()

def speak_wait(text):
    """Blocking speak — waits until finished"""
    print(f"Jarvis: {text}")
    try:
        audio = el_client.text_to_speech.convert(
            text=text,
            voice_id="onwK4e9ZLuTAKqWW03F9",
            model_id="eleven_turbo_v2",
            output_format="mp3_44100_128"
        )
        play_audio(audio)
    except Exception as e:
        print(f"ElevenLabs error: {e}")
        subprocess.run(['say', '-v', 'Daniel', text])

def wait_for_wake_word():
    """Listen for Jarvis wake word"""
    porcupine = pvporcupine.create(
        access_key=PICOVOICE_KEY,
        keywords=["jarvis"]
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
    """Listen for a voice command and return it as text"""
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=8, phrase_time_limit=15)
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            return None
        except sr.RequestError:
            speak("Sorry, I couldn't reach the speech service.")
            return None
        