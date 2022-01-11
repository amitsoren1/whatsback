from datetime import datetime
import pytz
import socketio

sio = socketio.Server(async_mode='eventlet', cors_allowed_origins='*')

users = {}
sid_mapper = {}

@sio.event
def connect(sid, environ, auth):
    print('connect ', sid)

@sio.event
def disconnect(sid):
    a=datetime.now(pytz.timezone('Asia/Kolkata'))
    last_seen = a.time().strftime("%I:%M %p") + " " + a.date().strftime("%d %b, %Y")
    users[sid] = last_seen
    sio.emit('went_offline', {'user_id': sid_mapper[sid], 'last_seen': last_seen})
    print(f"Client disconnected {sid}")

# @sio.event
# def my_broadcast_event(sid, message):
    

@sio.event
def join(sid, message):
    users[message["id"]] = "online"
    sid_mapper[sid] = message["id"]
    sio.enter_room(sid, str(message["id"]))
    sio.emit('went_online', {'user_id': sid_mapper[sid]})

@sio.event
def disconnect_request(sid):
    sio.disconnect(sid)
    print("disconnect", sid)

@sio.event
def get_user_status(sid, message):
    sio.emit("user_status", {"status_result": users[message["status_of"]]}, to=sid)

@sio.event
def send_message(sid, message):
    sio.emit("incoming_message", message["newMsgObject"], to=str(message["newMsgObject"]["sent_for"]))

@sio.event
def chat_read(sid, message):
    sio.emit("chat_read", message, to=str(message["chat_with"]))

@sio.event
def call_user(sid, message: dict):
    sio.emit("incoming_call", {
                            "signal": message["signal_data"],
                            "from": message["from"],
                            "call_type": message["call_type"]
                            },
            to=str(message["user_to_call"])
            )

@sio.event
def answer_call(sid, message: dict):
    sio.emit("call_acepted", message["signal"], to=str(message["to"]))
