#!/usr/bin/env python3

import sys
import struct
import socket
from xmlrpc.server import SimpleXMLRPCServer
from threading import Thread
import proxy

MAX_UDP_PAYLOAD = 65507

server = SimpleXMLRPCServer(("localhost", 5001), allow_none = True)
naming_proxy = proxy.TupleSpaceAdapter('http://localhost:8004')


def replicate_tuple_to_all(name, data):
    name_lists = naming_proxy._read_all()
    for namelist in name_lists:
        if namelist[0] != name:
            replicate_proxy = proxy.TupleSpaceAdapter(namelist[1])
            replicate_proxy._out(data)
    return "Sucessfully replicated\n"


def main(address = '224.0.0.1', port = '54323'):
    server_address = ('', int(port))

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(server_address)

    group = socket.inet_aton(address)
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    print(f"Listening on udp://{address}:{port}")

    try:
        while True:  #msg parsing
            data, _ = sock.recvfrom(MAX_UDP_PAYLOAD)
            notification = data.decode()
            print(notification)
            notifications_string = notification.split(' ')
            if notifications_string[1] == 'write':
                with open('log_data.txt', 'a') as f:
                    data = notifications_string[0]+','+notifications_string[2]
                    f.write(data)
                    replicate_tuple_to_all(notifications_string[0], notifications_string[2])

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
