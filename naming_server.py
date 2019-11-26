#!/usr/bin/env python3

import sys
import struct
import socket
from xmlrpc.server import SimpleXMLRPCServer
from threading import Thread
import proxy

naming_proxy = proxy.TupleSpaceAdapter('http://localhost:8004')


MAX_UDP_PAYLOAD = 65507

server = SimpleXMLRPCServer(("localhost", 5000), allow_none = True)

def getURI(name):
    return str(list(naming_proxy._rd(name))[1])

def recover_TupleSpace(URI):
    with open('log_data.txt', 'r') as f:
        for line in f.read():
            line_value = line.split(',')
            URI._out([line_value])

def main(address = '224.0.0.1', port = '54322'):
    server_address = ('', int(port))

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(server_address)

    group = socket.inet_aton(address)
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    print(f"Listening on udp://{address}:{port}")

    try:
        while True:
            data, _ = sock.recvfrom(MAX_UDP_PAYLOAD)
            notification = data.decode()
            print(notification)
            notifications_string = notification.split(' ')
            if notifications_string[1] == 'adapter':
                get_URI_proxy =  proxy.TupleSpaceAdapter(str(notifications_string[2]))
                print(naming_proxy._out([notifications_string[0], notifications_string[2]]))
                recover_TupleSpace(get_URI_proxy)

    except:
        sock.close()


def usage(program):
    print(f'Usage: {program} ADDRESS PORT', file=sys.stderr)
    sys.exit(1)

def server_handler():
    server.register_function(getURI, 'getURI')
    server.serve_forever()

t = Thread(target=server_handler)
t.start()

if __name__ == '__main__':
    main()
