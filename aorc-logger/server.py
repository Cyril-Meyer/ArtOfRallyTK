import time
import threading
import eventlet
import eventlet.wsgi
import socketio

default_output = open('output.csv', 'w')
output = default_output
LOGGER = False
sio = socketio.Server(logger=LOGGER)
app = socketio.WSGIApp(sio)


@sio.event(namespace='/users')
def carsInfo(sid, data):
    return
    print('carsInfo', sid, data)


@sio.event(namespace='/users')
def stagesInfo(sid, data):
    return
    print('stagesInfo', sid, data)


@sio.event(namespace='/users')
def loadLevel(sid, data):
    print('loadLevel', sid, data)
    return


@sio.event(namespace='/users')
def waypointsGathered(sid, data):
    return
    print('waypointsGathered', sid, data)


@sio.event(namespace='/users')
def stageUpdate(sid, data):
    global output
    # velocity = velocity * 0.6 * factor
    # factor = 3.6 for kmh, 2.237 for mph
    output.write(f"{str(time.time_ns() // 1000000)}," +
                 f"{round(float(data['carData']['drivetrain']['velocity']*0.6*3.6),2)}," +
                 f"{round(float(data['carData']['drivetrain']['rpm']),2)}," +
                 f"{int(data['carData']['drivetrain']['gear'])}\n")
    return
    print('stageUpdate', sid, data)


def record_30s():
    global output
    while True:
        filename = input()
        output = open(f'{filename}.csv', 'w')
        output.write('time,speed,rpm,gear\n')
        print(f'>{filename}.csv')
        time.sleep(30)
        print(f'<{filename}.csv')
        output.close()
        output = default_output


threading.Thread(target=record_30s,).start()
eventlet.wsgi.server(eventlet.listen(('', 4593)), app)
