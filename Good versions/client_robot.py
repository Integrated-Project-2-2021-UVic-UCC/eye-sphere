import socket
import sys

class Client():
    def __init__(self):
        self.name=input("Choose an username: ")
        self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.connect(('localhost',8080))
        self.send_name()
        self.loop_forever()
    
    def send_name(self):
        name='ROBT'+self.name
        sending(name,self.sock)

    def loop_forever(self):
        try:
            while True:
                msg=input('->')
                sending(msg,self.sock)

        except KeyboardInterrupt:
            print('Disconnectiong from de server...')
            sending('!DISCONNECT',self.sock)
            print('Disconnected!')
            sys.exit()
    

def sending(msg,client):
    header=6
    msg=msg.encode('utf8')
    msg_len=len(msg).to_bytes(header,'big')
    client.sendall(msg_len+msg)





client=Client()
    

    