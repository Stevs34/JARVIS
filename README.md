# J.A.R.V.I.S. 🤖
### Just A Rather Very Intelligent System
> A voice-activated AI home automation system inspired by Iron Man, built with Python and Arduino.

---

## 🎯 What It Does
JARVIS is a fully integrated smart home automation system that responds to voice commands to control your environment in real time. Say "Hey Jarvis" and control your lights, TV, music, and more using natural language.

---

## 🛠️ Tech Stack
| Technology | Purpose |
|---|---|
| Python | Core system brain |
| OpenAI GPT API | Natural language understanding |
| OpenAI Whisper | Local speech-to-text |
| Tuya/TinyTuya | Smart light control |
| pyvizio | Vizio TV control |
| Spotipy | Spotify control |
| Arduino Mega 2560 | Physical hardware control |
| Flask | Live web dashboard |
| SpeechRecognition | Voice input |

---

## 🏗️ System Architecture
```
Voice Input → Wake Word Detection → Speech to Text
                                          ↓
                                   GPT-4 AI Brain
                          ↙         ↓        ↓        ↘
                    Smart        Vizio     Spotify   Arduino
                    Lights        TV       Music     (LEDs/Fan)
                          ↘         ↓        ↓        ↙
                              Voice Response + Dashboard
```

## ⚙️ Hardware
- Arduino Mega 2560
- ELEGOO Ultimate Starter Kit
- Smart Life RGB LED lights (Tuya)
- Vizio Smart TV
- MacBook Air (system brain)

---

## 🚀 Features
- ✅ Wake word detection ("Hey Jarvis")
- ✅ Natural language command processing
- ✅ Smart light control (on/off, colour, brightness, scenes)
- ✅ TV control (power, volume, inputs)
- ✅ Spotify voice control
- ✅ Arduino physical LED and motor control
- ✅ Live web dashboard
- ✅ British AI voice response

---

## 📁 Project Structure
```
JARVIS/
├── main.py              # System brain
├── speech.py            # Voice input/output
├── ai.py                # GPT command processing
├── devices/
│   ├── lights.py        # Smart light control
│   ├── tv.py            # Vizio TV control
│   ├── alexa.py         # Alexa integration
│   ├── spotify.py       # Spotify control
│   └── arduino.py       # Arduino serial control
├── dashboard/
│   └── app.py           # Web dashboard
└── arduino/
    └── jarvis.ino       # Arduino firmware
```

---

## 🔧 Setup
1. Clone the repo
2. Create a virtual environment: `python3 -m venv jarvis-env`
3. Activate it: `source jarvis-env/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Add your API keys to `.env`
6. Run: `python3 main.py`

---

## 📋 Environment Variables
Create a `.env` file with the following:
```
OPENAI_API_KEY=your_key
TUYA_ACCESS_ID=your_key
TUYA_ACCESS_SECRET=your_key
TUYA_REGION=us
SPOTIFY_CLIENT_ID=your_key
SPOTIFY_CLIENT_SECRET=your_key
SPOTIFY_REDIRECT_URI=http://127.0.0.1:8888/callback
```

---

## 👨‍💻 Author
**Cole Steeves** — 2nd Year Mechanical Engineering Student
> Built as a portfolio project to demonstrate embedded systems, AI integration, and IoT architecture.

---

## 📄 License
MIT License
```
