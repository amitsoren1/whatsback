import socketio
import time
import threading  

sio = socketio.Server(async_mode='eventlet', cors_allowed_origins='*')

def asd():
    time.sleep(10)
    print("hoooohoooooooooooooooooo")

@sio.event
def connect(sid, environ, auth):
    print('connect ', sid)
    sio.emit("get_out", {"did": "you got out"}, to=sid)

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
