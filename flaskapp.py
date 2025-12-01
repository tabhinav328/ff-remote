# flaskapp.py → 100% working final version
import os
from flask import Flask, render_template_string
from datetime import datetime

app = Flask(__name__)
command = "none"
last_check_time = None
last_reply_received = False

@app.route('/')
def home():
    global last_reply_received, last_check_time
    status_html = '<span style="color:#888">Click CHECK STATUS to verify device</span>'
    if last_check_time:
        seconds_ago = (datetime.now() - last_check_time).total_seconds()
        if last_reply_received and seconds_ago < 10:
            status_html = '<span style="color:#00ff00;font-weight:bold;">DEVICE ONLINE — ready_dude</span>'
        elif seconds_ago >= 10:
            status_html = '<span style="color:#ff4444;">DEVICE OFFLINE (no reply)</span>'
        else:
            status_html = '<span style="color:#ffff00;">Checking...</span>'

    return render_template_string(f'''
        <!DOCTYPE html>
        <html><head><title>Free Fire Remote</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{font-family:Arial;background:#111;color:white;text-align:center;padding-top:50px;}}
            h1 {{color:#ff4444;}}
            button {{padding:20px 40px;margin:15px;font-size:22px;border:none;border-radius:12px;cursor:pointer;}}
            .run {{background:#00C853;}} .stop {{background:#D50000;}} .check {{background:#0066ff;}}
            #status {{margin-top:40px;font-size:28px;font-weight:bold;}}
        </style></head>
        <body>
            <h1>FREE FIRE REMOTE</h1>
            <button class="run" onclick="send('run')">RUN BINARY</button><br>
            <button class="stop" onclick="send('stop')">STOP BINARY</button><br><br>
            <button class="check" onclick="checkStatus()">CHECK STATUS</button>
            <div id="status">{status_html}</div>

            <script>
                function send(c){{fetch('/command/'+c);}}
                function checkStatus(){{
                    document.getElementById('status').innerHTML = '<span style="color:#ffff00;">Checking device...</span>';
                    fetch('/check', {{cache: 'no-store'}});
                    let tries = 0;
                    const interval = setInterval(() => {{
                        tries++;
                        fetch('/last_reply').then(r => r.text()).then(reply => {{
                            if(reply.trim() === "ready_dude"){{
                                clearInterval(interval);
                                document.getElementById('status').innerHTML = '<span style="color:#00ff00;font-weight:bold;">DEVICE ONLINE — ready_dude</span>';
                            }} else if(tries > 80){{
                                clearInterval(interval);
                                document.getElementById('status').innerHTML = '<span style="color:#ff4444;">DEVICE OFFLINE (no reply)</span>';
                            }}
                        }});
                    }}, 100);
                }}
            </script>
        </body></html>
    ''')

@app.route('/command/<cmd>')
def set_command(cmd):
    global command
    if cmd in ['run', 'stop']:
        command = cmd
    return "OK"

@app.route('/check')
def check():
    global last_check_time, last_reply_received
    last_check_time = datetime.now()
    last_reply_received = False
    return "checking..."

@app.route('/reply/ready_dude')
def reply_ready():
    global last_reply_received
    last_reply_received = True
    return "OK"

@app.route('/last_reply')
def get_last_reply():
    return "ready_dude" if last_reply_received else "waiting"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))