import socket, sys, select, threading, cv2, time, bluetooth, serial
import numpy as np


class Client():
    def __init__(self):
        self.data=b''
        self.connexion=False

        self.arduino2=serial.Serial("/dev/ttyUSB0",baudrate=9600)
        #Name: BASE_MOTOR          # MAC: 00:11:35:96:43:69
        self.BTname = "BASE_MOTOR"      # Device name
        self.BTaddr = "00:11:35:96:43:69"      # Device Address
        self.BTport = 1         # RFCOMM port


        self.name="robot1"#input("Choose an username: ")
        self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.connect(('192.168.1.146',8080))
        self.send_name()
        self.stop=True
        self.t=threading.Thread(target=send_img,args=[self,self.sock,lambda : self.stop])
        try:
            self.baseBT = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            self.baseBT.connect((self.BTaddr,self.BTport))
            #print("connected!")
        except bluetooth.btcommon.BluetoothError as err:
            # Error handler
            pass
        self.loop_forever()

    def start_video(self):
        self.cam1=cv2.VideoCapture(0)
        self.t.start()
        #self.cam2=cv2.VideoCapture(2)

    def send_name(self):
        name='ROBT'+self.name
        sending(name,self.sock)

    def loop_forever(self):
        try:
            while True:
                readers,writers,_=select.select([self.sock],[self.sock],[])
                for reader in readers:
                    if reader == self.sock:

                        data=recv_msg(self)
                        #print(f'[Server]\n{data}')
                        if self.connexion:
                            angle=data
                            data=recv_msg(self)
                            dir=bytes(data[:1],'utf8')
                            vel=data[1:]
                            new_angle=""
                            for e in angle:
                                new_angle=e+new_angle
                            self.arduino2.write(bytes("X"+new_angle+"Y",'utf8'))
                            #os.system("clear")
                            #print(f'Speed: {vel}, Direction: {dir}')
                            #print(f'Angle: {angle}')
                            try:
                                self.baseBT.send(dir+bytes(str(vel),'utf8'))
                            except bluetooth.btcommon.BluetoothError as err:
                                # Error handler
                                pass

                        if data == 'Connected successfully':
                            self.connexion=True
                            self.start_video()
                        if data=='!DISCONNECT':
                            self.arduino2.write(bytes("X"+"09"+"Y",'utf8'))
                            try:
                                self.baseBT.send(b'R'+bytes(str(0),'utf8'))
                            except bluetooth.btcommon.BluetoothError as err:
                                # Error handler
                                pass
                            self.connexion=False
                            self.stop=False
                            self.t.join()
                            self.cam1.release()
                            self.sock.close()
                            time.sleep(1)
                            self.sock.connect(('192.168.1.146',8080))
                            self.send_name()
                        

                        

        except KeyboardInterrupt:
            print('Disconnectiong from de server...')
            sending('!DISCONNECT',self.sock)
            print('Disconnected!')
            self.sock.close()
            sys.exit()
        except ConnectionResetError:
            self.sock.close()
            time.sleep(1)
            self.sock.connect(('192.168.1.146',8080))
            self.send_name()

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

def send_img(rob,client,stop):
    while stop():
        header=6
        frame1=rob.cam1.read()[1]
        #frame2=rob.cam2.read()[1]
        img_1=cv2.imencode(".jpeg",frame1,[cv2.IMWRITE_JPEG_QUALITY,20])[1].tobytes()
        #img_2=cv2.imencode(".jpeg",frame2,[cv2.IMWRITE_JPEG_QUALITY,20])[1].tobytes()
        #header = f"{len(img_1):6.0f}"
        msg_len1=len(img_1).to_bytes(header,'big')
        #msg_len2=len(img_2).to_bytes(header,'big')
        client.sendall(msg_len1+img_1)
        #client.sendall(msg_len2+img_2)

def sending(msg,client):
    header=6
    msg=msg.encode('utf8')
    msg_len=len(msg).to_bytes(header,'big')
    client.sendall(msg_len+msg)

client=Client()
    

    