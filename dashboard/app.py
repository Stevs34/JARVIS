from flask import Flask, jsonify, render_template_string
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from devices import spotify
from skills import get_weather

app = Flask(__name__)

state = {
    "status": "Online",
    "last_command": "None",
    "last_action": "None",
    "lights": "Unknown",
    "tv": "Unknown",
    "spotify": "Nothing playing",
    "weather": "Loading...",
    "command_history": []
}

def update_state(key, value):
    state[key] = value
    if key == "last_command" and value != "None":
        state["command_history"].insert(0, value)
        state["command_history"] = state["command_history"][:5]

DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>J.A.R.V.I.S.</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }

        html, body {
            height: 100%;
            overflow: hidden;
            background-color: #0a0a0f;
            color: #00d4ff;
            font-family: 'Courier New', monospace;
        }

        .container {
            height: 100vh;
            display: grid;
            grid-template-rows: auto 1fr;
            padding: 15px;
            gap: 12px;
        }

        .header {
            display: grid;
            grid-template-columns: 1fr auto 1fr;
            align-items: center;
            padding-bottom: 12px;
            border-bottom: 1px solid #00d4ff33;
        }

        .header-left {
            font-size: 0.8em;
            color: #00d4ff88;
        }

        .header-center {
            text-align: center;
        }

        .header-center h1 {
            font-size: 1.8em;
            letter-spacing: 0.3em;
            text-shadow: 0 0 20px #00d4ff;
        }

        .header-center p {
            font-size: 0.65em;
            color: #00d4ff88;
            letter-spacing: 0.2em;
        }

        .header-right {
            text-align: right;
        }

        .clock {
            font-size: 1.4em;
            text-shadow: 0 0 10px #00d4ff;
        }

        .date {
            font-size: 0.75em;
            color: #00d4ff88;
        }

        .status-badge {
            display: inline-block;
            background: #00d4ff22;
            border: 1px solid #00d4ff;
            border-radius: 20px;
            padding: 3px 12px;
            font-size: 0.7em;
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }

        .grid {
            display: grid;
            grid-template-columns: 1.2fr 1fr 1fr;
            grid-template-rows: 1fr 1fr 1fr;
            gap: 12px;
            height: 100%;
        }

        .card {
            background: #0d1117;
            border: 1px solid #00d4ff33;
            border-radius: 10px;
            padding: 15px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            overflow: hidden;
        }

        .card h2 {
            font-size: 0.65em;
            letter-spacing: 0.2em;
            color: #00d4ff88;
            margin-bottom: 8px;
            text-transform: uppercase;
        }

        .card .value {
            font-size: 1em;
            color: #ffffff;
            flex: 1;
        }

        .span-col-2 { grid-column: span 2; }
        .span-row-2 { grid-row: span 2; }

        .last-command {
            font-size: 1.1em;
            color: #00d4ff;
            font-style: italic;
        }

        .spotify-info {
            display: flex;
            align-items: center;
            gap: 12px;
            flex: 1;
        }

        .sound-bars {
            display: flex;
            align-items: flex-end;
            gap: 3px;
            height: 25px;
            flex-shrink: 0;
        }

        .bar {
            width: 4px;
            background: #00d4ff;
            border-radius: 2px;
            height: 5px;
        }

        .bar.playing {
            animation: bounce 0.8s infinite ease-in-out;
        }

        .bar:nth-child(2) { animation-delay: 0.15s; }
        .bar:nth-child(3) { animation-delay: 0.3s; }
        .bar:nth-child(4) { animation-delay: 0.45s; }
        .bar:nth-child(5) { animation-delay: 0.6s; }

        @keyframes bounce {
            0%, 100% { height: 4px; }
            50% { height: 22px; }
        }

        .controls {
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
            margin-top: 10px;
        }

        button {
            background: #00d4ff22;
            border: 1px solid #00d4ff;
            color: #00d4ff;
            padding: 6px 12px;
            border-radius: 5px;
            cursor: pointer;
            font-family: 'Courier New', monospace;
            font-size: 0.75em;
            transition: all 0.2s;
        }

        button:hover {
            background: #00d4ff44;
            box-shadow: 0 0 10px #00d4ff44;
        }

        .history-item {
            font-size: 0.78em;
            color: #00d4ff88;
            padding: 3px 0;
            border-bottom: 1px solid #00d4ff11;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .history-item:first-child {
            color: #ffffff;
            font-size: 0.85em;
        }

        .device-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 5px 0;
            border-bottom: 1px solid #00d4ff11;
            font-size: 0.85em;
        }

        .device-status {
            color: #ffffff;
            font-size: 0.85em;
        }

        .weather-temp {
            font-size: 1.8em;
            color: #ffffff;
            line-height: 1;
        }

        .weather-desc {
            font-size: 0.8em;
            color: #00d4ff88;
            margin-top: 4px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="header-left">
                <div class="status-badge">● ONLINE</div>
            </div>
            <div class="header-center">
                <h1>J.A.R.V.I.S.</h1>
                <p>JUST A RATHER VERY INTELLIGENT SYSTEM</p>
            </div>
            <div class="header-right">
                <div class="clock" id="clock">--:-- --</div>
                <div class="date" id="date">---</div>
            </div>
        </div>

        <div class="grid">
            <!-- Row 1 -->
            <div class="card span-col-2">
                <h2>Last Command</h2>
                <div class="value last-command" id="last-command">Awaiting input...</div>
            </div>

            <div class="card">
                <h2>Weather — Fredericton</h2>
                <div class="weather-temp" id="weather-temp">--°</div>
                <div class="weather-desc" id="weather-desc">Loading...</div>
            </div>

            <!-- Row 2 -->
            <div class="card span-col-2">
                <h2>Now Playing</h2>
                <div class="spotify-info">
                    <div class="sound-bars" id="sound-bars">
                        <div class="bar"></div>
                        <div class="bar"></div>
                        <div class="bar"></div>
                        <div class="bar"></div>
                        <div class="bar"></div>
                    </div>
                    <div class="value" id="spotify">Nothing playing</div>
                </div>
                <div class="controls">
                    <button onclick="sendCommand('previous')">⏮</button>
                    <button onclick="sendCommand('pause')">⏸</button>
                    <button onclick="sendCommand('play')">▶</button>
                    <button onclick="sendCommand('next')">⏭</button>
                </div>
            </div>

            <div class="card">
                <h2>Devices</h2>
                <div class="device-row">
                    <span>💡 Lights</span>
                    <span class="device-status" id="lights">Unknown</span>
                </div>
                <div class="device-row">
                    <span>📺 TV</span>
                    <span class="device-status" id="tv">Unknown</span>
                </div>
                <div class="controls" style="margin-top:8px">
                    <button onclick="sendCommand('movie_mode')">🎬</button>
                    <button onclick="sendCommand('study_mode')">📚</button>
                    <button onclick="sendCommand('party_mode')">🎉</button>
                    <button onclick="sendCommand('good_morning')">🌅</button>
                </div>
            </div>

            <!-- Row 3 -->
            <div class="card span-col-2">
                <h2>Last Action</h2>
                <div class="value" id="last-action">None</div>
            </div>

            <div class="card">
                <h2>Command History</h2>
                <div id="history">
                    <div class="history-item">No commands yet</div>
                </div>
            </div>
        </div>
    </div>

    <script>
        function updateClock() {
            const now = new Date();
            document.getElementById('clock').textContent = now.toLocaleTimeString('en-US', {hour:'2-digit', minute:'2-digit', second:'2-digit'});
            document.getElementById('date').textContent = now.toLocaleDateString('en-US', {weekday:'long', month:'long', day:'numeric'});
        }
        setInterval(updateClock, 1000);
        updateClock();

        function fetchState() {
            fetch('/state')
                .then(r => r.json())
                .then(data => {
                    document.getElementById('last-command').textContent = data.last_command;
                    document.getElementById('last-action').textContent = data.last_action;
                    document.getElementById('lights').textContent = data.lights;
                    document.getElementById('tv').textContent = data.tv;
                    document.getElementById('spotify').textContent = data.spotify;

                    const bars = document.querySelectorAll('.bar');
                    const isPlaying = data.spotify !== 'Nothing playing' && data.spotify !== 'Paused';
                    bars.forEach(bar => {
                        isPlaying ? bar.classList.add('playing') : bar.classList.remove('playing');
                    });

                    if (data.command_history && data.command_history.length > 0) {
                        document.getElementById('history').innerHTML = data.command_history
                            .map(cmd => `<div class="history-item">> ${cmd}</div>`)
                            .join('');
                    }

                    if (data.weather && data.weather !== 'Loading...') {
                        const parts = data.weather.split(' ');
                        document.getElementById('weather-temp').textContent = parts[1] + '°C';
                        document.getElementById('weather-desc').textContent = data.weather;
                    }
                });
        }

        function fetchWeather() {
            fetch('/weather')
                .then(r => r.json())
                .then(data => {
                    if (data.weather) {
                        document.getElementById('weather-desc').textContent = data.weather;
                    }
                });
        }

        function sendCommand(command) {
            fetch('/command/' + command)
                .then(r => r.json())
                .then(() => setTimeout(fetchState, 1000));
        }

        fetchState();
        fetchWeather();
        setInterval(fetchState, 5000);
        setInterval(fetchWeather, 300000);
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(DASHBOARD_HTML)

@app.route("/state")
def get_state():
    try:
        state["spotify"] = spotify.get_current_track()
    except:
        pass
    return jsonify(state)

@app.route("/weather")
def weather():
    try:
        w = get_weather()
        state["weather"] = w
        return jsonify({"weather": w})
    except:
        return jsonify({"weather": "Unavailable"})

@app.route("/command/<action>")
def run_command(action):
    try:
        if action == "play":
            spotify.play()
            state["spotify"] = spotify.get_current_track()
        elif action == "pause":
            spotify.pause()
            state["spotify"] = "Paused"
        elif action == "next":
            spotify.next_track()
        elif action == "previous":
            spotify.previous_track()
        state["last_action"] = action
        return jsonify({"status": "ok", "action": action})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

def run_dashboard():
    app.run(host="0.0.0.0", port=8080, debug=False, use_reloader=False)
