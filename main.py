from speech import speak, listen
from ai import ask_jarvis

speak("Good evening. JARVIS online. All systems ready.")

while True:
    command = listen()
    if command:
        print(f"Processing: {command}")
        response = ask_jarvis(command)
        speak(response)
    if command == "stop":
        speak("Goodbye sir.")
        break
