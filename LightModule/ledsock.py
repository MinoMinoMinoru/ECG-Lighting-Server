import socket,time,math

class LedSocket:
    def __init__(self, sock = None):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self):
        self.sock.connect(('172.20.11.68', 14649))

    def close(self):
        self.sock.close()

    def update(self):
        msg = "UPDATE\n"
        MSGLEN = len(msg)
        totalsent = 0
        while totalsent < MSGLEN:
            sent = self.sock.send(msg[totalsent:].encode("utf-8"))
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent
        return totalsent

    def sendAll(self, led):
        msg = 'SET_ALL %d,%d,%d,%d,\n' % (led[0], led[1], led[2], led[3])
        MSGLEN = len(msg)
        totalsent = 0
        while totalsent < MSGLEN:
            sent = self.sock.send(msg[totalsent:].encode("utf-8"))
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent
        return totalsent

    def sendSingle(self, lightid, led):
        msg = 'SET_SINGLE %d %d,%d,%d,%d,\n' % (lightid, led[0], led[1], led[2], led[3])
        MSGLEN = len(msg)
        totalsent = 0
        while totalsent < MSGLEN:
            sent = self.sock.send(msg[totalsent:].encode("utf-8"))
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent
        return totalsent

    def sendMulti(self, led):
        for i in range(len(led)):
            self.sendSingle(i, led[i])

    def sendMessage(self, msg):
        self.sock.send(msg)
