import serial
import time
import os
import bluetooth
import subprocess

#Open serial
arduino=serial.Serial("/dev/ttyACM0",baudrate=9600)
#arduino2=serial.Serial("/dev/ttyUSB0",baudrate=9600)
#Name: BASE_MOTOR          # MAC: 00:11:35:96:43:69
name = "BASE_MOTOR"      # Device name
addr = "00:11:35:96:43:69"      # Device Address
port = 1         # RFCOMM port

def bt_connect():
    passkey = "0000" # passkey of the device you want to connect

    # kill any "bluetooth-agent" process that is already running
    subprocess.call("kill -9 `pidof bluetooth-agent`",shell=True)

    # Start a new "bluetooth-agent" process where XXXX is the passkey
    status = subprocess.call("bluetooth-agent " + passkey + " &",shell=True)

    # Now, connect in the same way as always with PyBlueZ


def read():
    a=arduino.read()
    while a!=b'X':
        a=arduino.read()
    a=arduino.read()
    valX=b''
    while a!=b'Y':
        valX+=a
        a=arduino.read()
    a=arduino.read()
    valY=b''
    while a!=b'X':
        valY+=a
        a=arduino.read()
    return int(valX), int(valY)


#Calibration
max=1024
min=0
zeroX,zeroY=read()

def trans2deg(num,zero=zeroY):
    if num>zero:
        deg=((num-zero)*90)/(1024-zero)+90
    else:
        deg=(num*90)/zero
    return deg

def trans2speed(num,zero=zeroX):
    if num>zero:
        dir=b'R'
        speed=12-((num-zero)*10)/(1024-zero)
    else:
        dir=b'L'
        speed=(num*10)/zero+2
    if 9<speed<=12:
        dir=b'R'
        speed=0
    return int(speed),dir

try:
    s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    s.connect((addr,port))
    #print("connected!")
except bluetooth.btcommon.BluetoothError as err:
        # Error handler
        pass

#Main Program
while True:
    dataX,dataY=read()
    os.system("clear")
    angleY=int(trans2deg(dataY))
    speedX,direccion=trans2speed(dataX)
    print(f'X: {dataX}, ZeroX is: {zeroX}, Speed: {speedX}')
    print(f'Y: {dataY}, ZeroY is: {zeroY}, Angle: {angleY}')
    try:
        s.send(direccion+bytes(str(speedX),'utf8'))
    except bluetooth.btcommon.BluetoothError as err:
        # Error handler
        pass
 
    