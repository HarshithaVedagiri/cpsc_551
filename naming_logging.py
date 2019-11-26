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
count = 1
def replicate_tuple_to_all(name, data):
    namelists = []
    for i in range(0, count):
        name_list_row = naming_proxy._rd(count)
        namelists.append(name_list_row)
    for namelist in namelists:
        if namelist[1] != name:
            replicate_proxy = proxy.TupleSpaceAdapter((int, namelist[2], str))
            replicate_proxy._out(data)
    return "Sucessfully replicated\n"


def getURI(name):
    v = naming_proxy._rd((int, name ,str))
    return str(v)

def recover_TupleSpace(URI):
    with open('log_data.txt', 'r') as f:
        for line in f.read():
            line_value = line.split(',')
            URI._out([line_value])

def main(address = '224.0.0.1', port = '54322'):
    server_address = ('', int(port))
    global count
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
            namecheck = None
            notifications_string = notification.split(' ')
            print("inside while")
            if notifications_string[1] == 'adapter':
                print("inside adapter")
                get_URI_proxy =  proxy.TupleSpaceAdapter(str(notifications_string[2]))
                if count > 1:
                    namecheck = naming_proxy._in((int, notifications_string[0], str))

                if namecheck:
                    print(naming_proxy._out((namecheck[0], notifications_string[0], notifications_string[2])))
                else:
                    print(naming_proxy._out((count, notifications_string[0], notifications_string[2])))
                    count += 1
                recover_TupleSpace(get_URI_proxy)

            elif notifications_string[1] == 'write' and notifications_string[0] != 'naming_server_ts':
                print("inside wrte")
                with open('log_data.txt', 'a') as f:
                    data = notifications_string[0]+','+notifications_string[2]
                    f.write(data)
                    replicate_tuple_to_all(notifications_string[0], notifications_string[2])
    except Exception as e:
        print(e)
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
