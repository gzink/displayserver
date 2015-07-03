import zmq
import json

class DisplayClient:
    socket = None

    def __init__(self, port = 5757):
        context = zmq.Context()
        self.socket = context.socket(zmq.REQ)
        self.socket.connect ("tcp://127.0.0.1:%s" % port)

    def send_message_standby(self, message):
        msg = {
            'type': 'standby',
            'message': message
        }
        self._send_to_socket(msg)

    def send_message_flash(self, message, timeout = 10):
        msg = {
            'type': 'flash',
            'message': message,
            'timeout': timeout
        }
        self._send_to_socket(msg)

    def _send_to_socket(self, msg):
        self.socket.send (json.dumps(msg))
        self.socket.recv()

if __name__ == '__main__':
    client = DisplayClient()
    client.send_message_standby("abctest")
    client.send_message_flash(["hallo", "welt", "katze", "Blupfsajfisajfisajfisaji"], 3)
