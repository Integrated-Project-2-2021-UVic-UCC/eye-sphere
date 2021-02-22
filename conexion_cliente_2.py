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
##    while len(data) < payload_size:
##        packet = miSocket.recv(4*1024)
##        if not packet:
##            break
##        data+=packet
##    packed_msg_size=data[:payload_size]
##    data=data[payload_size:]
##    msg_size=struct.unpack("Q",packed_msg_size)[0]
##
    while len(data) < msg_size:
        data+=miSocket.recv(msg_size)
        
    frame_data=data[:msg_size]
    data=data[msg_size:]

    #frame_data = miSocket.recv(640*480*3)

    frame = np.frombuffer(frame_data,np.uint8)
    frame = frame.reshape((480, 640, 3))
    cv2.imshow("Client Video",frame)
    key=cv2.waitKey(1) and 0xFF
    print(key)
    if key == ord('q'):
        print(key)
        break
miSocket.close()

    
"""
    ret, frame=cap.read()
    #cv2.imshow('VisorOriginal',frame)
    miSocket=socket.socket() #creamos objeto socket
    #data=input("mensaje: ")
    msg=pickle.dumps(frame)#bytes(data,'utf-8')
    miSocket.send(msg)
    respuesta = miSocket.recv(1024)#1024 hace referencia la bufer, es decir 1024 bytes
    #respuesta=list(str(respuesta,'ascii'))
    print(respuesta)
    miSocket.close()
        
    #si pulsamos q finalizamos el bucle
    if cv2.waitKey(1) and (0xFF==ord('q')):
        break
"""

"""
cap.release()
cv2.destroyAllWindows()
    msg=bytes(data,'utf-8')
    miSocket.send(msg)
    respuesta = miSocket.recv(1024)#1024 hace referencia la bufer, es decir 1024 bytes
    #respuesta=list(str(respuesta,'ascii'))
    print(respuesta)
    miSocket.close()
"""
