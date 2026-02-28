from flask import Flask, jsonify, render_template_string
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from devices import spotify

app = Flask(__name__)

# Shared state — updates as Jarvis runs
state = {
    "status": "Online",
    "last_command": "None",
    "last_action": "None",
    "lights": "Unknown",
    "tv": "Unknown",
    "spotify": "Nothing playing"
}

def update_state(key, value):
    state[key] = value

DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>J.A.R.V.I.S.</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            background-color: #0a0a0f;
            color: #00d4ff;
            font-family: 'Courier New', monospace;
            min-height: 100vh;
            padding: 20px;
        }

        .header {
            text-align: center;
            padding: 30px 0 20px;
            border-bottom: 1px solid #00d4ff33;
            margin-bottom: 30px;
        }

        .header h1 {
            font-size: 2.5em;
            letter-spacing: 0.3em;
            text-shadow: 0 0 20px #00d4ff;
        }

        .header p {
            font-size: 0.8em;
            color: #00d4ff88;
            letter-spacing: 0.2em;
            margin-top: 5px;
        }

        .status-badge {
            display: inline-block;
            background: #00d4ff22;
            border: 1px solid #00d4ff;
            border-radius: 20px;
            padding: 5px 15px;
            font-size: 0.8em;
            margin-top: 10px;
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }

        .grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            max-width: 800px;
            margin: 0 auto;
        }

        .card {
            background: #0d1117;
            border: 1px solid #00d4ff33;
            border-radius: 10px;
            padding: 20px;
        }

        .card h2 {
            font-size: 0.75em;
            letter-spacing: 0.2em;
            color: #00d4ff88;
            margin-bottom: 10px;
            text-transform: uppercase;
        }

        .card .value {
            font-size: 1.1em;
            color: #ffffff;
        }

        .card.full-width {
            grid-column: 1 / -1;
        }

        .spotify-card {
            display: flex;
            align-items: center;
            gap: 15px;
        }

        .spotify-icon {
            font-size: 2em;
        }

        .controls {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            margin-top: 15px;
        }

        button {
            background: #00d4ff22;
            border: 1px solid #00d4ff;
            color: #00d4ff;
            padding: 8px 16px;
            border-radius: 5px;
            cursor: pointer;
            font-family: 'Courier New', monospace;
            font-size: 0.85em;
            transition: all 0.2s;
        }

        button:hover {
            background: #00d4ff44;
            box-shadow: 0 0 10px #00d4ff44;
        }

        .last-command {
            font-size: 1.2em;
            color: #00d4ff;
            font-style: italic;
        }

        .footer {
            text-align: center;
            margin-top: 30px;
            color: #00d4ff33;
            font-size: 0.75em;
            letter-spacing: 0.1em;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>J.A.R.V.I.S.</h1>
        <p>JUST A RATHER VERY INTELLIGENT SYSTEM</p>
        <div class="status-badge" id="status">● ONLINE</div>
    </div>

    <div class="grid">
        <div class="card full-width">
            <h2>Last Command</h2>
            <div class="value last-command" id="last-command">Awaiting input...</div>
        </div>

        <div class="card">
            <h2>Last Action</h2>
            <div class="value" id="last-action">None</div>
        </div>

        <div class="card">
            <h2>Lights</h2>
            <div class="value" id="lights">Unknown</div>
        </div>

        <div class="card full-width">
            <h2>Now Playing</h2>
            <div class="spotify-card">
                <div class="spotify-icon">🎵</div>
                <div class="value" id="spotify">Nothing playing</div>
            </div>
            <div class="controls">
                <button onclick="sendCommand('previous')">⏮ Prev</button>
                <button onclick="sendCommand('pause')">⏸ Pause</button>
                <button onclick="sendCommand('play')">▶ Play</button>
                <button onclick="sendCommand('next')">⏭ Next</button>
            </div>
        </div>

        <div class="card">
            <h2>TV</h2>
            <div class="value" id="tv">Unknown</div>
        </div>

        <div class="card">
            <h2>Quick Modes</h2>
            <div class="controls">
                <button onclick="sendCommand('movie_mode')">🎬 Movie</button>
                <button onclick="sendCommand('study_mode')">📚 Study</button>
                <button onclick="sendCommand('party_mode')">🎉 Party</button>
            </div>
        </div>
    </div>

    <div class="footer">
        <p>STARK INDUSTRIES — JARVIS v1.0 — AUTO REFRESH 5s</p>
    </div>

    <script>
        function fetchState() {
            fetch('/state')
                .then(r => r.json())
                .then(data => {
                    document.getElementById('last-command').textContent = data.last_command;
                    document.getElementById('last-action').textContent = data.last_action;
                    document.getElementById('lights').textContent = data.lights;
                    document.getElementById('tv').textContent = data.tv;
                    document.getElementById('spotify').textContent = data.spotify;
                });
        }

        function sendCommand(command) {
            fetch('/command/' + command)
                .then(r => r.json())
                .then(data => {
                    console.log(data);
                    setTimeout(fetchState, 1000);
                });
        }

        // Auto refresh every 5 seconds
        fetchState();
        setInterval(fetchState, 5000);
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
    