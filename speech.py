import speech_recognition as sr
import subprocess

def speak(text):
    """Jarvis speaks back to you using Daniel voice"""
    print(f"Jarvis: {text}")
    subprocess.run(['say', '-v', 'Daniel', '-a', 'MacBook Air Speakers', text])


def listen():
    """Listen for a voice command and return it as text"""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = recognizer.listen(source, timeout=5)
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
        