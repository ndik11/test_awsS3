#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket

sock = socket.socket()
sock.connect(('localhost', 8007))
sock.send('hello, world!')

data = sock.recv(1024)
sock.close()

print data