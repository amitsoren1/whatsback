import socketio

sio = socketio.Server(async_mode='eventlet', cors_allowed_origins='*')

@sio.event
def connect(sid, environ, auth):
    print('connect ', sid)

@sio.event
def join(sid, message):
    sio.enter_room(sid, str(message["id"]))

@sio.event
def disconnect_request(sid):
    sio.disconnect(sid)
    print("disconnect", sid)

@sio.event
def send_message(sid, message):
    sio.emit("incoming_message", message["newMsgObject"], to=str(message["newMsgObject"]["sent_for"]))

@sio.event
def chat_read(sid, message):
    sio.emit("chat_read", message, to=str(message["chat_with"]))
