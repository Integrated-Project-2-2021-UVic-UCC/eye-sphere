import socket                       #Importamos la librerya socket
import sys                          #exit() parar el programa
import select
import cv2
import numpy as np
import threading

class Client():                     
    def __init__(self,name):
        self.data=b''
        self.connexion=False
        #self.t=threading.Thread(target=self.start_video)
        self.name=name#input("Choose an username: ")                     #asignamos un nombre con el que el servidor nos conocera
        self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)  #inicia la comunicacion red con los protocolos especificados
        self.sock.connect(('192.168.1.146',8080))                       #se conecta a la direccion i el purto del servidor
        self.send_name()                                            
    
    def send_name(self):
        name='USER'+self.name
        sending(name,self.sock)
    
    # def start_video(self):
    #     while True:
    #         img=recv_img(self)
    #         cv2.imshow('video',img)
    #         if cv2.waitKey(1) == ord('q'):
    #             break
    def send_msg(self,msg):
        sending(msg,self.sock)
    
    def recieve_msg(self):
        return recv_msg(self)
        
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

def recv_img(client):
    header_size=6
    while len(client.get_data())<header_size:
        client.build_data(client.sock.recv(header_size))
    
    header=client.get_data()[:header_size]
    client.save_data(client.get_data()[header_size:])
    data_size=int.from_bytes(header,'big')

    while len(client.get_data()) < data_size:
        client.build_data(client.sock.recv(data_size))
    
    #final_img=np.frombuffer(client.get_data()[:data_size],np.uint8)
    #final_img=cv2.imdecode(final_img,cv2.IMREAD_UNCHANGED)
    final_img=client.get_data()[:data_size]
    client.save_data(client.get_data()[data_size:])
    
    return final_img

def sending(msg,client):
    header=6
    msg=msg.encode('utf8')                          #Pasamos el codigo de texto ('ascii') a bytes ('utf8')
    msg_len=len(msg).to_bytes(header,'big')
    client.sendall(msg_len+msg)


#client=Client()                             #Creamos objeto de la clase cliente
    

    