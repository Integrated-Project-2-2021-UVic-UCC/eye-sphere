import socket
import sys
import select
import cv2
import numpy as np

class Client():
    def __init__(self):
        self.data=b''
        self.connexion=False

        self.name=input("Choose an username: ")
        self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.connect(('localhost',8080))
        self.send_name()
        self.loop_forever()

    def start_video(self):
        self.cam1=cv2.VideoCapture(0)

    def send_name(self):
        name='ROBT'+self.name
        sending(name,self.sock)

    def loop_forever(self):
        try:
            while True:
                readers,writers,_=select.select([sys.stdin,self.sock],[self.sock],[])
                for reader in readers:
                    if reader == self.sock:

                        data=recv_msg(self)
                        print(f'[Server]\n{data}')

                        if data == 'Connected successfully':
                            self.connexion=True
                            self.start_video()
                        if data=='!DISCONNECT':
                            self.connexion=False
                            
                    else:
                        msg=sys.stdin.readline()[:-1]
                        sending(msg,self.sock)
                for _ in writers:
                    if self.connexion:
                        send_img(self.cam1,self.sock)
                    else:
                        pass
                        #self.cam1.release()
                        

        except KeyboardInterrupt:
            print('Disconnectiong from de server...')
            sending('!DISCONNECT',self.sock)
            print('Disconnected!')
            sys.exit()

    def build_data(self,data):
        self.data+=data

    def save_data(self,data):
        self.data=data

    def get_data(self):
        return self.data


def recv_msg(client):
    header_size=6
    while len(client.get_data())<header_size:
        client.build_data(client.sock.recv(header_size))
    
    header=client.get_data()[:header_size]
    client.save_data(client.get_data()[header_size:])
    data_size=int.from_bytes(header,'big')

    while len(client.get_data()) < data_size:
        client.build_data(client.sock.recv(data_size))
    
    final_data=client.get_data()[:data_size].decode('utf8')
    client.save_data(client.get_data()[data_size:])
    return final_data

def send_img(cam,client):
    header=6
    frame=cam.read()[1]
    img_1=cv2.imencode(".jpeg",frame,[cv2.IMWRITE_JPEG_QUALITY,20])[1].tobytes()
    #header = f"{len(img_1):6.0f}"
    msg_len=len(img_1).to_bytes(header,'big')
    client.sendall(msg_len+img_1)

def sending(msg,client):
    header=6
    msg=msg.encode('utf8')
    msg_len=len(msg).to_bytes(header,'big')
    client.sendall(msg_len+msg)

client=Client()
    

    