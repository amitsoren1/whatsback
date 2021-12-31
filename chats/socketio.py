import socketio
import time
import threading

sio = socketio.Server(async_mode='eventlet', cors_allowed_origins='*')

connected_clients = {}

def asd():
    time.sleep(10)
    print("hoooohoooooooooooooooooo")


@sio.event
def connect(sid, environ, auth):
    # print('connect ', sid)
    # sio.enter_room(sid, sid+str())
    # sio.emit("get_out", {"did": "you got out"}, to=sid)
    sio.emit("join_user")

@sio.event
def join(sid, message):
    # print(message, "gggggggg")
    sio.enter_room(sid, str(message["id"]))
    # sio.emit("hoodone", {"did": "hoodone ind"}, to=str(message["id"]))

@sio.event
def disconnect_request(sid):
    sio.disconnect(sid)
    print("disconnect", sid)

@sio.event
def dothing(sid, message):
    print("hooing")
    sio.emit("hoodone", {"did": "hoodone ind"}, to=sid)
    # sio.start_background_task(asd)
    T1 = threading.Thread(target = asd)
    T1.start()
    print("triggered")

@sio.event
def send_message(sid, message):
    print(message)
    # print("hooing")
    # sio.emit("hoodone", {"did": "hoodone ind"}, to=sid)
    # # sio.start_background_task(asd)
    # T1 = threading.Thread(target=new_message, args=(message,))
    # T1.start()
    # print()
    sio.emit("incoming_message", message["newMsgObject"], to=str(message["newMsgObject"]["sent_for"]))
    print("triggered")


@sio.event
def chat_read(sid, message):
    print(message)
    expcted = {
        "chat_with": 1,
        "reader": 3
    }
    # T1 = threading.Thread(target=update_read_messages, args=(message["reader"], message["chat_with"]))
    # T1.start()
    # print()
    sio.emit("chat_read", message, to=str(message["chat_with"]))
    print("triggered2")
