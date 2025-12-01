# flaskapp.py → AUTO shows online + buttons appear instantly
import os
from flask import Flask, render_template_string
from datetime import datetime, timedelta

app = Flask(__name__)
command = "none"
last_alive = None   # updated by Android app every few seconds

@app.route('/')
def home():
    global last_alive, command
    is_online = last_alive and (datetime.now() - last_alive < timedelta(seconds=8))

    status = "DEVICE OFFLINE"
    color = "#ff4444"
    buttons = "display:none;"

    if is_online:
        status = "DEVICE ONLINE"
        color = "#00ff00"
        buttons = ""

    return render_template_string(f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Free Fire Remote</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body {{font-family:Arial;background:#111;color:white;text-align:center;padding-top:80px;}}
                h1 {{color:#ff4444;}}
                button {{padding:25px 50px;margin:20px;font-size:26px;border:none;border-radius:15px;}}
                .run {{background:#00C853;}} .stop {{background:#D50000;}}
                #status {{font-size:32px;font-weight:bold;margin:40px;color:{color};}}
                .buttons {{ {buttons} }}
            </style>
        </head>
        <body>
            <h1>FREE FIRE REMOTE</h1>
            <div id="status">{status}</div>
            <div class="buttons">
                <button class="run" onclick="fetch('/run')">RUN BINARY</button><br><br>
                <button class="stop" onclick="fetch('/stop')">STOP BINARY</button>
            </div>
        </body>
        </html>
    ''')

@app.route('/alive')
def alive():
    global last_alive
    last_alive = datetime.now()
    return "OK"

@app.route('/run')
def run(): 
    global command; command = "run"; return "OK"
@app.route('/stop')
def stop(): 
    global command; command = "stop"; return "OK"
@app.route('/status')
def status(): 
    return command

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
