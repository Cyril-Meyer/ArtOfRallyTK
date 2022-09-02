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
parser.add_argument('--logs', action='store_true')
args = parser.parse_args()
gearbox = json.load(args.settings)
print(gearbox, type(gearbox))

sio = socketio.Server(logger=False)
app = socketio.WSGIApp(sio)

gear = 0
speed = 0
rpm = 0
if args.logs:
    output = open('automated-manual-transmission/logs.csv', 'w')
    output.write('time,speed,rpm,gear\n')


@sio.event(namespace='/users')
def stageUpdate(sid, data):
    global output
    global gear, speed, rpm
    # velocity = velocity * 0.6 * factor
    # factor = 3.6 for kmh, 2.237 for mph
    speed = float(data['carData']['drivetrain']['velocity']*0.6*3.6)
    rpm = float(data['carData']['drivetrain']['rpm'])
    gear = int(data['carData']['drivetrain']['gear'])

    if args.logs:
        output.write(f"{str(time.time_ns() // 1000000)}," +
                     f"{round(speed,2)}," +
                     f"{round(rpm, 2)}," +
                     f"{gear}\n")
    return


def thread_amt():
    global gearbox, gear, speed, rpm
    while True:
        if gear >= 2:
            x = amt.apply(gearbox, gear-1, speed, rpm)
            if x > 0:
                print("↑")
                time.sleep(0.1)
            elif x < 0:
                print("↓")
                time.sleep(0.1)

        time.sleep(0.01)


threading.Thread(target=thread_amt,).start()
eventlet.wsgi.server(eventlet.listen(('', 4593)), app)
