import socket
import cv2
import pickle
import struct
import numpy as np

miSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # creamos el objeto socket
#miSocket.bind( ('25.4.178.254',25565) ) #('localhost',8000)establecemos donde abriremos el servidor
miSocket.bind( ('localhost',8000)) #establecemos donde abriremos el servidor

miSocket.listen(5) #establece el numero de dispositivos que puede escuchar
print("listening...")
while True:
    conexion, addr = miSocket.accept() #se queda esperando una conexion, cuando la detecta, la acepta i nes dice quien se ha conectado
    #conexion es el objeto cliente que se nos ha conectado i adr su direcion ip
    print("nueva connexion establecida en direccion: ",end=" ")
    if conexion:
        video=cv2.VideoCapture(0)
        while (video.isOpened()):
            img,frame=video.read()
            conexion.sendall(frame.tobytes())
            cv2.imshow('ServerVideo',frame)
            key=cv2.waitKey(1) and 0xFF
            if key == ord('q'):
                conexion.close()

