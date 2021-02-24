#Codigo streaming CLIENTE comprimiendo video jpeg

import socket
import cv2
import pickle
import struct
import numpy as np

miSocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#miSocket.connect( ('25.2.1.212', 25500) ) #nos conectamos a un servidor, asi que nos asignamos como clientes
miSocket.connect( ('localhost',8000) ) #nos conectamos a un servidor, asi que nos asignamos como clientes

data = b""
header_size =6
while True:
    # read header.
    while len(data) < header_size:
        data += miSocket.recv(header_size)

    header = data[:header_size]
    data = data[header_size:]
    msg_size = int(header)
    
    while len(data) < msg_size:
        data+=miSocket.recv(msg_size)
        
    frame_data=data[:msg_size]
    data=data[msg_size:]

    frame = np.frombuffer(frame_data,np.uint8)
    frame=cv2.imdecode(frame,cv2.IMREAD_UNCHANGED)
    cv2.imshow("Client Video",frame)
    key=cv2.waitKey(1) and 0xFF
    if key == ord('q'):
        break
miSocket.close()
