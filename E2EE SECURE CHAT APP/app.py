from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import json
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

clients = []

LOG_FILE = "chat_logs.txt"

# Create empty log file if not present
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w") as f:
        f.write("[]")

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('public_key')
def handle_public_key(pub_key):
    clients.append({'sid': request.sid, 'pub_key': pub_key})
    if len(clients) == 2:
        emit('peer_public_key', clients[1]['pub_key'], room=clients[0]['sid'])
        emit('peer_public_key', clients[0]['pub_key'], room=clients[1]['sid'])

@socketio.on('message')
def handle_message(data):
    # Save encrypted message to file (server cannot decrypt)
    with open(LOG_FILE, "r+") as f:
        logs = json.load(f)
        logs.append(data)
        f.seek(0)
        json.dump(logs, f, indent=2)
        f.truncate()

    # Forward encrypted message to other client
    emit('message', data, broadcast=True, include_self=False)

if __name__ == '__main__':
    socketio.run(app, debug=True)
