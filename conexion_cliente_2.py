import socket
#import numpy as np
import cv2
import pickle
import struct
import numpy as np

miSocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#miSocket.connect( ('25.4.178.254', 25565) ) #nos conectamos a un servidor, asi que nos asignamos como clientes
miSocket.connect( ('localhost',8000) ) #nos conectamos a un servidor, asi que nos asignamos como clientes

data = b""
payload_size = struct.calcsize("Q")
msg_size = 640*480*3
while True:
    
    while len(data) < msg_size:
        data+=miSocket.recv(msg_size)
        
    frame_data=data[:msg_size]
    data=data[msg_size:]

    frame = np.frombuffer(frame_data,np.uint8)
    frame = frame.reshape((480, 640, 3))
    cv2.imshow("Client Video",frame)
    key=cv2.waitKey(1) and 0xFF
    print(key)
    if key == ord('q'):
        print(key)
        break
miSocket.close()

