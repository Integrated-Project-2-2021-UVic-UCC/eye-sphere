import socket
import threading
import sys
import pickle
import cv2
import numpy as np

class Cliente():
        """docstring for Cliente"""
        def __init__(self, host="servermuac.ddns.net", port=21):
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.connect((str(host), int(port)))
                #self.sock.send(pickle.dumps("cam1"))
                self.video=cv2.VideoCapture(0)
                msg_recv = threading.Thread(target=self.msg_recv)
                stream=threading.Thread(target=self.stream)

                msg_recv.daemon = True
                msg_recv.start()

                stream.daemon = True
                stream.start()
                while True:
                        msg = input('->')
                        if msg != 'salir':
                                #self.sock.sendall(self.packet)
                                print(len(self.packet))
                        else:
                                self.sock.close()
                                sys.exit()
        def stream(self):
                while True:
                        frame=self.video.read()[1]
                        cv2.imshow('videoCam',frame)
                        buf=cv2.imencode('.jpeg',frame,[cv2.IMWRITE_JPEG_QUALITY,20])[1].tobytes()#imencode devuelve 2 valores, pero nos quedamos con el 2nd que es lo que nos interesa
                        header = bytes(f"{len(buf):6.0f}",'utf-8')
                        self.packet=header+buf
                        self.sock.sendall(self.packet)
                        key=cv2.waitKey(1) and 0xFF
                        if key == ord('q'):
                                self.sock.close()
                                break
        def msg_recv(self):
                while True:
                        try:
                                data = self.sock.recv(1024)
                                if data:
                                        print(pickle.loads(data))
                        except:
                                pass

c = Cliente()
