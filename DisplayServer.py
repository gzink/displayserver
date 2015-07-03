#!/usr/bin/python

import zmq
import json
import time

from ssd1803a import ssd1803a

port = 5757

class DisplayServer:
    msg_standby = 'DisplayServer ready on port %s' % port
    msg_flash = None
    flash_timeout = 0
    prev_message = None

    # ZeroMQ
    socket = None
    poller = None

    ssd = None

    def __init__(self, port):
        self.ssd = ssd1803a()

        context = zmq.Context()
        self.socket = context.socket(zmq.REP)
        self.socket.bind("tcp://127.0.0.1:%s" % port)

        self.poller = zmq.Poller()
        self.poller.register(self.socket, zmq.POLLIN)

    def update_message(self):
        if int(time.time()) <= self.flash_timeout:
            message = self.msg_flash
        else:
            message = self.msg_standby

        if self.prev_message == message:
            return

        # Send message to display
        if type(message) is list:
            self.ssd.dis_print_lines(message)
        else:
            self.ssd.cmd_clear()
            self.ssd.dis_print(message)

        self.prev_message = message

    def handle_request(self, message):
        if message['type'] == 'standby':
            self.msg_standby = message['message']
        if message['type'] == 'flash':
            self.msg_flash = message['message']
            self.flash_timeout = int(time.time()) + message['timeout']

    def loop(self):
        self.update_message()
        evts = self.poller.poll(1000)
        if len(evts) > 0:
            message_encoded = self.socket.recv()
            message = json.loads(message_encoded)
            if not type(message) is dict or not 'type' in message or not 'message' in message:
                self.socket.send('invalid request')
            else:
                self.handle_request(message)
                self.socket.send('okay')

if __name__ == '__main__':
    serv = DisplayServer(port)
    while True:
        serv.loop()
