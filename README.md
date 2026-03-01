# J.A.R.V.I.S.
### Just A Rather Very Intelligent System

> *"At ease, JARVIS. I've got this."*  
> *"As you wish, sir. Though I do hope that's true."*

A fully functional AI home automation system inspired by Iron Man, built with Python. JARVIS uses voice commands to control smart home devices, play music, answer questions, and manage your life — all with a dry British wit.

---

## ⚡ Features

### 🎙️ Voice & AI
- Wake word detection — say **"Jarvis"** to activate
- Human-like voice powered by **ElevenLabs**
- **GPT-4o-mini** powered natural language understanding
- Persistent memory — remembers things you tell it
- Follow-up questions without repeating the wake word
- Iron Man personality with dry British wit

### 🏠 Smart Home Control
- **RGB Smart Lights** — on/off, colours, brightness, scene modes
- **Vizio TV** — on/off, volume, mute
- **Spotify** — play, pause, skip, volume, play by song/playlist, multi-room

### 💻 Mac Control
- Volume control, mute, lock screen, sleep
- Open any application by voice
- Media play/pause/skip
- Send iMessages by voice
- Open directions in Apple Maps
- Check battery level

### 📊 Information
- Live weather for Fredericton
- Stock prices (real-time)
- Wikipedia search
- NHL/NBA/NFL sports scores
- Top Canadian news headlines
- Language translation
- Math calculations
- Jokes and random facts
- Current time and date

### ⏰ Productivity
- Set timers by voice
- Add and check reminders
- Persistent memory across sessions
- Boot diagnostics on startup

### 🖥️ Interface
- Animated AI orb — changes colour based on state
- Live web dashboard at http://127.0.0.1:8080
- Command history log
- Real-time Spotify now playing
- Quick mode buttons

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| AI Brain | OpenAI GPT-4o-mini |
| Voice Output | ElevenLabs Turbo v2 |
| Voice Input | Google Speech Recognition |
| Wake Word | Picovoice Porcupine |
| Smart Lights | TinyTuya (Tuya/Smart Life) |
| TV Control | pyvizio |
| Music | Spotify Web API (spotipy) |
| Dashboard | Flask |
| Visual Orb | Tkinter |
| Hardware | Arduino Mega 2560 |
| Memory | JSON persistent storage |
| Language | Python 3.14 |

---

## 🏗️ Architecture
JARVIS/
├── main.py              # Main control loop
├── speech.py            # Voice I/O and wake word
├── ai.py                # GPT-4o brain
├── start_jarvis.sh      # Startup script
├── core/
│   ├── skills.py        # Weather, stocks, Wikipedia, etc.
│   └── memory.py        # Persistent memory and reminders
├── devices/
│   ├── lights.py        # Tuya/Smart Life RGB lights
│   ├── tv.py            # Vizio TV control
│   ├── spotify.py       # Spotify multi-device control
│   └── arduino.py       # Arduino serial communication
├── dashboard/
│   └── app.py           # Flask web dashboard
├── ui/
│   └── orb.py           # Animated AI orb
└── arduino/
└── jarvis.ino       # Arduino firmware
---

## 🚀 Setup

### Prerequisites
- Python 3.10+
- Homebrew (Mac)
- PortAudio: brew install portaudio
- ffmpeg: brew install ffmpeg
- Tkinter: brew install python-tk

### Installation

git clone https://github.com/Stevs34/JARVIS.git
cd JARVIS
python3 -m venv jarvis-env
source jarvis-env/bin/activate
pip install -r requirements.txt

### Environment Variables

Create a .env file in the root directory:

OPENAI_API_KEY=your_key_here
ELEVENLABS_API_KEY=your_key_here
PICOVOICE_ACCESS_KEY=your_key_here
SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret
SPOTIFY_REDIRECT_URI=http://127.0.0.1:8888/callback
TUYA_ACCESS_ID=your_access_id
TUYA_ACCESS_SECRET=your_access_secret
TUYA_REGION=us
TUYA_LIGHT_DEVICE_ID=your_device_id
TUYA_LIGHT_LOCAL_KEY=your_local_key
TUYA_LIGHT_IP=your_light_ip
VIZIO_IP=your_tv_ip
VIZIO_AUTH_TOKEN=your_auth_token
OPENWEATHER_API_KEY=your_key_here
CITY=Fredericton

### Running

source jarvis-env/bin/activate
python3 main.py

Or say "Hey Siri, Jarvis" if you have the Siri Shortcut set up.

---

## 🎮 Voice Commands

| Command | Action |
|---|---|
| "Turn on the lights" | Lights on |
| "Set lights to red" | RGB colour change |
| "Movie mode" | Dim purple lights + TV on |
| "Study mode" | Bright white lights |
| "Party mode" | Pink lights |
| "Turn on the TV" | TV power on |
| "Volume up" | TV volume up |
| "Play some music" | Spotify play |
| "Play [song name]" | Spotify song search |
| "What's the weather?" | Live weather |
| "What's Apple stock?" | Real-time stock price |
| "Search Wikipedia for [topic]" | Wikipedia summary |
| "What are the NHL scores?" | Live sports scores |
| "Set a timer for 10 minutes" | Countdown timer |
| "Remind me to [task]" | Add reminder |
| "What are my reminders?" | List reminders |
| "What's my battery level?" | Mac battery |
| "Open Spotify" | Launch app |
| "Lock my screen" | Mac lock |
| "Tell me a joke" | Random joke |
| "Tell me a random fact" | Random fact |
| "Translate [text] to French" | Translation |
| "Get directions to [place]" | Apple Maps |
| "Send a message to [name]" | iMessage |

---

## 🔌 Hardware

| Component | Purpose |
|---|---|
| MacBook Air M2 | Main processing unit |
| Smart Life RGB Strip | Room lighting |
| Vizio SmartCast TV | Display control |
| Amazon Echo devices | Multi-room audio |
| Arduino Mega 2560 | Physical LED/button control |
| L298N Motor Driver | Fan speed control |

---

## 🗺️ Roadmap

- [x] Wake word detection
- [x] ElevenLabs voice
- [x] GPT-4 brain with memory
- [x] Smart Life lights
- [x] Vizio TV control
- [x] Spotify multi-device
- [x] Web dashboard
- [x] Animated AI orb
- [x] Boot diagnostics
- [ ] Arduino physical controls
- [ ] Alexa announcements
- [ ] Computer vision
- [ ] Calendar integration

---

## 👨‍💻 Author

**Cole Steeves** — 2nd Year Mechanical Engineering, University of New Brunswick

Built as a portfolio project demonstrating embedded systems, API integration, and AI development.

---

*"The mark of a good AI assistant is not what it can do, but what it allows you to accomplish."*