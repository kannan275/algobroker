import time
import zmq
import algobroker
import msgpack

def client():
    context = zmq.Context()
    zmq_socket = context.socket(zmq.PUSH)
    zmq_socket.bind(algobroker.ports.dispatcher)
    # Start your result manager and workers before you start your
    work_message = { 'action' : 'log',
                     'item' : 'hello' }
    zmq_socket.send(msgpack.packb(work_message))
    work_message = { 'action' : 'alert',
                     'type' : 'sms',
                     'dst'  : 'trader1',
                     'text' : 'hello' }
    zmq_socket.send(msgpack.packb(work_message))

    zmq_socket = context.socket(zmq.PUSH)
    zmq_socket.bind(algobroker.ports.plivo)
    work_message = { 'action' : 'alert',
                     'type' : 'sms',
                     'dst'  : 'trader1',
                     'text' : 'hello' }
    zmq_socket.send(msgpack.packb(work_message))
client()
