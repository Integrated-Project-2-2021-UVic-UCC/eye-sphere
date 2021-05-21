from numpy.core.arrayprint import set_string_function
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5 import uic
from cliente_basico_library import *
#from mobileConexionGui import *
import threading

class FinPpal(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("userWindow.ui",self)
        self.setWindowTitle("Mobile Setup")
        self.finVideo=FinVideo(self)
        self.shell.setEnabled(False)
        self.refresh.setEnabled(False)
        self.robotConnect.setEnabled(False)
        self.robotID.setEnabled(False)
        #Variables de usuario
        self.name=""

        #Setup timer Camera
        self.timer=QtCore.QTimer()
        #self.timer.start(20) faltapensar donde va!!!!

        #Connected Signals
        self.userConnect.clicked.connect(self.saveUserame)
        self.robotConnect.clicked.connect(self.connectRobot)
        self.refresh.clicked.connect(self.getRobotList)
        self.timer.timeout.connect(self.finVideo.video)
    
    def saveUserame(self):
        self.name=self.username.text()
        try:
            self.shell.setPlainText("Trying to connect to the server...")
            self.cliente=Client(self.name)
            self.shell.appendPlainText(f"Connection complete as {self.name}")
            self.shell.appendPlainText(f"Openning robot menu...")
            self.getRobotList()
            self.refresh.setEnabled(True)
            self.robotConnect.setEnabled(True)
            self.robotID.setEnabled(True)
        except:
            self.shell.appendPlainText(f"Connection Failed!")
    
    def getRobotList(self):
        self.cliente.send_msg("!LIST")
        s=self.cliente.recieve_msg()
        print(s)
        self.shell.setPlainText("RobotList:")
        self.shell.appendPlainText(f"{s}")
    def connectRobot(self): 
        robID=self.robotID.text()
        self.cliente.send_msg("!CONNECT")
        self.cliente.send_msg(robID)
        self.shell.appendPlainText(f"Trying to connect to {robID}...")
        response=self.cliente.recieve_msg()
        if response=="1":
            self.shell.appendPlainText("Connection Successfully")
            self.finVideo.show()
            self.finVideo.inici_t()
            #self.timer.start(20)
        else:
            self.shell.appendPlainText("Connection Failed")
    def video(self):
        self.finVideo.video(recv_img(self.cliente))

class FinVideo(QMainWindow):
    def __init__(self,parent):
        super().__init__(parent)
        uic.loadUi("video.ui",self)
        self.setWindowTitle("Mobile Setup")
        #self.cam1=cv2.VideoCapture(0)
        self.t=threading.Thread(target=self.video)

    def inici_t(self):
        self.t.start()

    def video(self):
        #frame=self.cam1.read()[1]
        #img_1=cv2.imencode(".jpeg",frame,[cv2.IMWRITE_JPEG_QUALITY,80])[1].tobytes()
        while True:
            #finestra.cliente.send_msg("1")
            img_1=recv_img(finestra.cliente)
            qImg = QtGui.QImage.fromData(img_1)
            pixmap01 = QtGui.QPixmap.fromImage(qImg)
            self.marcoL.setPixmap(pixmap01)
            self.marcoR.setPixmap(pixmap01)

        
app=QApplication([])
finestra=FinPpal()
finestra.show()
app.exec_()