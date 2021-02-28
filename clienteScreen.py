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
                
                msg_recv = threading.Thread(target=self.msg_recv)

                msg_recv.daemon = True
                msg_recv.start()

                while True:
                        msg = input('->')
                        if msg != 'salir':
                                self.sock.send(pickle.dumps(msg))
                        else:
                                self.sock.close()
                                sys.exit()

        def msg_recv(self):
                self.data=b""
                header_size=6
                while True:
                        #try:
                        while len(self.data) < header_size:
                                self.data += self.sock.recv(header_size)

                        header = self.data[:header_size]
                        self.data = self.data[header_size:]
                        msg_size = int(header)

                        while len(self.data) < msg_size:
                                self.data+=self.sock.recv(msg_size)

                        frame_data=self.data[:msg_size]
                        self.data=self.data[msg_size:]

                        frame = np.frombuffer(frame_data,np.uint8)
                        frame=cv2.imdecode(frame,cv2.IMREAD_UNCHANGED)
                        cv2.imshow("Client Video",frame)
                        key=cv2.waitKey(1) and 0xFF
                        if key == ord('q'):
                                break
                        #except:
                        #        pass

c = Cliente()
