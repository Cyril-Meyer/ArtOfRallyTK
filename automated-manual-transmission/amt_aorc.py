import argparse
import json
import time
import threading
import eventlet.wsgi
import socketio
import amt

parser = argparse.ArgumentParser()
parser.add_argument('settings', help='json file containing gearbox settings',
                    type=argparse.FileType('r', encoding='UTF-8'))
args = parser.parse_args()
gearbox = json.load(args.settings)
print(gearbox, type(gearbox))

sio = socketio.Server(logger=False)
app = socketio.WSGIApp(sio)

gear = 0
speed = 0
rpm = 0


@sio.event(namespace='/users')
def stageUpdate(sid, data):
    global gear, speed, rpm
    # velocity = velocity * 0.6 * factor
    # factor = 3.6 for kmh, 2.237 for mph
    speed = float(data['carData']['drivetrain']['velocity']*0.6*3.6)
    rpm = float(data['carData']['drivetrain']['rpm'])
    gear = int(data['carData']['drivetrain']['gear'])
    return


def thread_amt():
    global gearbox, gear, speed, rpm
    while True:
        if gear >= 2:
            x = amt.apply(gearbox, gear-1, speed, rpm)
            if x > 0:
                print("↑")
                time.sleep(1.0)
            elif x < 0:
                print("↓")
                time.sleep(1.0)

        time.sleep(0.01)


threading.Thread(target=thread_amt,).start()
eventlet.wsgi.server(eventlet.listen(('', 4593)), app)
