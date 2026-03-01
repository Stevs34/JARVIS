import speech_recognition as sr
import subprocess
import pvporcupine
import pyaudio
import struct
import os
import threading
from dotenv import load_dotenv

load_dotenv()

PICOVOICE_KEY = os.getenv("PICOVOICE_ACCESS_KEY")

# Initialize recognizer once globally — not every time we listen
recognizer = sr.Recognizer()
recognizer.pause_threshold = 1.5
recognizer.phrase_threshold = 0.3
recognizer.non_speaking_duration = 0.8
recognizer.energy_threshold = 300
recognizer.dynamic_energy_threshold = False  # Stops it recalibrating every time

def speak(text):
    """Jarvis speaks back — non blocking so listening can resume faster"""
    print(f"Jarvis: {text}")
    subprocess.Popen(['say', '-v', 'Daniel', '-a', 'MacBook Air Speakers', text])

def speak_wait(text):
    """Blocking speak — use when Jarvis needs to finish before continuing"""
    print(f"Jarvis: {text}")
    subprocess.run(['say', '-v', 'Daniel', '-a', 'MacBook Air Speakers', text])

def wait_for_wake_word():
    """Listen for 'Jarvis' wake word"""
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
             