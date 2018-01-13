from aiohttp import web
import socketio
from test import EM
from test import Connect
from test import PM
from test import Manager
from test import SM
from test import System
# employee=EM()
# manager=Manager()
# personel=PM()
# god=SM()
sys=System()
cur=0
sio = socketio.AsyncServer()
app = web.Application()
login={}
sio.attach(app)


@sio.on('connect', namespace='/db')
def connect(sid, environ):
    print("connect ", sid)

@sio.on('update', namespace='/db')
async def message(sid, data):
    print("message ", data)
    if login[sid]:
        return login[sid].update(data)

@sio.on('insert', namespace='/db')
async def message(sid, data):
    print("message ", data)
    if login[sid]:
        return login[sid].insert(data)

@sio.on('delete', namespace='/db')
async def message(sid, data):
    print("message ", data)
    if login[sid]:
        return login[sid].delete(data)

@sio.on('e_login', namespace='/db')
async def message(sid, data):
    print("message ", data)
    e=EM()
    result=e.login(data)
    if result:
        login[sid]=e
    return result
@sio.on('m_login', namespace='/db')
async def message(sid, data):
    m = Manager()
    result = m.login(data)
    if result:
        login[sid] = m
    return result
@sio.on('p_login', namespace='/db')
async def message(sid, data):
    p = PM()
    result = p.login(data)
    if result:
        login[sid] = p
    return result
@sio.on('s_login', namespace='/db')
async def message(sid, data):
    s = SM()
    result = s.login(data)
    if result:
        login[sid] = s
    return result
@sio.on('change_info', namespace='/db')
async def message(sid, data):
    if login[sid]:
        return login[sid].change_info(data)
@sio.on('attendance_search', namespace='/db')
async def message(sid, data):
    if login[sid]:
        return login[sid].attendance_search(data)
@sio.on('tl_search', namespace='/db')
async def message(sid, data):
    if login[sid]:
        return login[sid].tl_search(data)
@sio.on('e_search', namespace='/db')
async def message(sid, data):
    if login[sid]:
        return login[sid].e_search(data)
@sio.on('sum_a_search', namespace='/db')
async def message(sid, data):
    if login[sid]:
        return login[sid].sum_a_search(data)

@sio.on('d_search', namespace='/db')
async def message(sid, data):
    if login[sid]:
        return login[sid].d_search(data)
@sio.on('log_search', namespace='/db')
async def message(sid, data):
    if login[sid]:
        return login[sid].log_search(data)


@sio.on('disconnect', namespace='/db')
def disconnect(sid):
    print('disconnect ', sid)
    login.pop(sid)

if __name__ == '__main__':
    web.run_app(app)