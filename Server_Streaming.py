import socket
import cv2
import pickle
import struct
import numpy as np

miSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # creamos el objeto socket
#miSocket.bind( ('25.4.178.254',25565) ) #('localhost',8000)establecemos donde abriremos el servidor
miSocket.bind( ('localhost',8000)) #establecemos donde abriremos el servidor
#miSocket.bind( ('192.168.43.213',8000) )


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
            #frame = frame[:,:,1] #uncoment to get color image
            buf=cv2.imencode('.jpeg',frame,[cv2.IMWRITE_JPEG_QUALITY,10])[1].tobytes()#imencode devuelve 2 valores, pero nos quedamos con el 2nd que es lo que nos interesa
            header = bytes(f"{len(buf):6.0f}",'utf-8')
            conexion.sendall(header+buf)
            cv2.imshow('ServerVideo',frame)
            key=cv2.waitKey(1) and 0xFF
            if key == ord('q'):
                conexion.close()

