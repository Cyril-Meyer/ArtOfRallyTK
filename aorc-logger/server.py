import eventlet
import eventlet.wsgi
import socketio

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
    print('stageUpdate', sid, data)


eventlet.wsgi.server(eventlet.listen(('', 4593)), app)
