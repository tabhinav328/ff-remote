import os, json
from flask import Flask, render_template_string, request
from datetime import datetime, timedelta

app = Flask(__name__)

STATE_FILE = "state.json"

command = "none"
last_alive = None


# ---------------- PERSISTENCE ----------------
def load_state():
    global command, last_alive
    if os.path.exists(STATE_FILE):
        try:
            data = json.load(open(STATE_FILE))
            command = data.get("command", "none")
            ts = data.get("last_alive")
            if ts:
                last_alive = datetime.fromtimestamp(ts)
        except:
            pass

def save_state():
    try:
        with open(STATE_FILE, "w") as f:
            json.dump({
                "command": command,
                "last_alive": last_alive.timestamp() if last_alive else None
            }, f)
    except:
        pass


load_state()

#lol
# ---------------- UI ----------------
@app.route("/")
def home():
    global last_alive, command

    is_online = last_alive and (datetime.now() - last_alive < timedelta(seconds=15))

    status = "DEVICE OFFLINE"
    color = "#ff4444"
    buttons_style = "display:none;"

    if is_online:
        status = "DEVICE ONLINE"
        color = "#00ff00"
        buttons_style = ""

    return render_template_string(f"""
    <html><head><title>Remote Panel</title>
    <style>
        body {{background:#111;color:white;font-family:Arial;text-align:center;padding-top:80px;}}
        #status {{font-size:34px;font-weight:bold;color:{color};margin-bottom:30px;}}
        button {{padding:25px 50px;font-size:26px;border-radius:15px;border:none;margin:20px;cursor:pointer;}}
        .run {{background:#00C853;}} .stop{{background:#D50000;}}
    </style>
    </head><body>
        <h1>REMOTE CONTROL</h1>
        <div id='status'>{status}</div>
        <div style="{buttons_style}">
            <button class="run" onclick="fetch('/run')">RUN BINARY</button><br>
            <button class="stop" onclick="fetch('/stop')">STOP BINARY</button>
        </div>
        <script>
            setInterval(()=>location.reload(),5000)
        </script>
    </body></html>
    """)


# ---------------- API ENDPOINTS ----------------

@app.route("/alive", methods=["POST"])
def alive():
    global last_alive
    last_alive = datetime.now()
    save_state()
    print(f"[HEARTBEAT] Received at {last_alive}")
    return "OK"


@app.route("/run")
def run():
    global command
    command = "run"
    save_state()
    return "OK"


@app.route("/stop")
def stop():
    global command
    command = "stop"
    save_state()
    return "OK"


@app.route("/status")
def status():
    return command


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT',5000)))
