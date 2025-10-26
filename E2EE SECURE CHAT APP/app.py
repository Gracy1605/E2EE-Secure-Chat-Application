from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

users = {}  # sid -> public_key

@app.route("/")
def index():
    return render_template("index.html")

@socketio.on("public_key")
def handle_public_key(pub_key):
    users[request.sid] = pub_key
    # send all existing keys to the new client
    for sid, key in users.items():
        if sid != request.sid:
            emit("peer_public_key", key, room=request.sid)
    # broadcast the new key to existing clients
    for sid, key in users.items():
        if sid != request.sid:
            emit("peer_public_key", pub_key, room=sid)

@socketio.on("message")
def handle_message(data):
    # broadcast to all clients except sender
    for sid in users:
        if sid != request.sid:
            emit("message", data, room=sid)

@socketio.on("disconnect")
def handle_disconnect():
    users.pop(request.sid, None)

if __name__ == "__main__":
    socketio.run(app, debug=True)

