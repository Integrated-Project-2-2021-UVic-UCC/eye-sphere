from numpy.core.arrayprint import set_string_function
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5 import uic
from cliente_basico_library import *
import threading, serial

class FinPpal(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("userWindow.ui",self)
        self.setWindowTitle("Mobile Setup")
        self.finVideo=FinVideo(self)
        self.cliente=None
        self.shell.setEnabled(False)
        self.refresh.setEnabled(False)
        self.robotConnect.setEnabled(False)
        self.robotID.setEnabled(False)
        #Variables de usuario
        self.name=""

        #Connected Signals
        self.userConnect.clicked.connect(self.saveUserame)
        self.robotConnect.clicked.connect(self.connectRobot)
        self.refresh.clicked.connect(self.getRobotList)
    
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
        else:
            self.shell.appendPlainText("Connection Failed")
    def video(self):
        self.finVideo.video(recv_img(self.cliente))
    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        if self.cliente!=None:
            self.cliente.send_msg("!DISCONNECT")
        return super().closeEvent(a0)


class FinVideo(QMainWindow):
    def __init__(self,parent):
        super().__init__(parent)
        uic.loadUi("video.ui",self)
        self.setWindowTitle("Mobile Setup")
        self.stop=True
        self.t=threading.Thread(target=self.video,args=(lambda:self.stop,))
        self.t2=threading.Thread(target=self.joy,args=(lambda:self.stop,))
        # self.timer=QtCore.QTimer(self)
        # self.timer.timeout.connect(self.joy)
        # self.timer2=QtCore.QTimer(self)
        # self.timer2.timeout.connect(self.video)

    def inici_t(self):
        self.t.start()
        #self.timer2.start(0.01)
        self.arduino=serial.Serial("/dev/ttyACM0",baudrate=9600)
        self.zeroX,self.zeroY=self.read()
        self.t2.start()
        #self.timer.start(0.01)

    def video(self,stop):      #Threads option
        while stop():
            img_1=recv_img(finestra.cliente)
            qImg = QtGui.QImage.fromData(img_1)
            pixmap01 = QtGui.QPixmap.fromImage(qImg)
            self.marcoL.setPixmap(pixmap01)
            self.marcoR.setPixmap(pixmap01)

    # def video(self):            #Timer Option
    #     img_1=recv_img(finestra.cliente)
    #     qImg = QtGui.QImage.fromData(img_1)
    #     pixmap01 = QtGui.QPixmap.fromImage(qImg)
    #     self.marcoL.setPixmap(pixmap01)
    #     self.marcoR.setPixmap(pixmap01)

    def joy(self,stop):
        while stop():
            dataX,dataY=self.read()
            angleY=int(self.trans2deg(dataY,self.zeroY))
            speedX,direccion=self.trans2speed(dataX,self.zeroX)
            #self.box.setPlainText(f"Angle: {angleY}")
            finestra.cliente.send_msg(str(angleY))
            #self.box.appendPlainText(f"Dir: {direccion}, Speed: {speedX}")
            finestra.cliente.send_msg(direccion+str(speedX))
    
    def read(self):
        a=self.arduino.read()
        while a!=b'X':
            a=self.arduino.read()
        a=self.arduino.read()
        valX=b''
        while a!=b'Y':
            valX+=a
            a=self.arduino.read()
        a=self.arduino.read()
        valY=b''
        while a!=b'X':
            valY+=a
            a=self.arduino.read()
        return int(valX), int(valY)

    def trans2deg(self,num,zero):
        if num>zero:
            deg=((num-zero)*90)/(1024-zero)+90
        else:
            deg=(num*90)/zero
        return deg

    def trans2speed(self,num,zero):
        if num>zero:
            dir='R'
            speed=12-((num-zero)*10)/(1024-zero)
        else:
            dir='L'
            speed=(num*10)/zero+2
        if 9<speed<=12:
            dir='R'
            speed=0
        return int(speed),dir

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        finestra.cliente.send_msg("!DISCONNECT")
        # self.timer2.stop()
        # self.timer.stop()
        self.stop=False
        self.t.join()
        self.t2.join()
        finestra.cliente.sock.close()
        return super().closeEvent(a0)

        
app=QApplication([])
finestra=FinPpal()
finestra.show()
app.exec_()