import socket                       #Importamos la librerya socket
import sys                          #exit() parar el programa
import select

class Client():                     
    def __init__(self):
        self.data=b''
        self.name=input("Choose an username: ")                     #asignamos un nombre con el que el servidor nos conocera
        self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)  #inicia la comunicacion red con los protocolos especificados
        self.sock.connect(('localhost',8080))                       #se conecta a la direccion i el purto del servidor
        self.send_name()                                            
        self.loop_forever()
    
    def send_name(self):
        name='USER'+self.name
        sending(name,self.sock)

    def loop_forever(self):
        try:
            while True:
                readers,_,_=select.select([sys.stdin,self.sock],[],[])
                for reader in readers:
                    if reader == self.sock:
                        data=recv_msg(self)
                        print(f'[Server]\n{data}')
                    else:
                        msg=sys.stdin.readline()[:-1]
                        command=msg.split()[0]
                        if command == '!CONNECT':
                            sending(command,self.sock)
                            name=msg.split()[1]
                            sending(name,self.sock)
                        else:
                            sending(msg,self.sock)

        except KeyboardInterrupt:
            print('Disconnectiong from de server...')
            sending('!DISCONNECT',self.sock)
            print('Disconnected!')
            sys.exit()
        
    def build_data(self,data):
        self.data+=data

    def save_data(self,data):
        self.data=data

    def get_data(self):
        return self.data
    
def recv_msg(client):
    header_size=6
    while len(client.get_data())<header_size:
        client.build_data(client.sock.recv(header_size))
    
    header=client.get_data()[:header_size]
    client.save_data(client.get_data()[header_size:])
    data_size=int.from_bytes(header,'big')

    while len(client.get_data()) < data_size:
        client.build_data(client.sock.recv(data_size))
    
    final_data=client.get_data()[:data_size].decode('utf8')
    client.save_data(client.get_data()[data_size:])
    return final_data


def sending(msg,client):
    header=6
    msg=msg.encode('utf8')                          #Pasamos el codigo de texto ('ascii') a bytes ('utf8')
    msg_len=len(msg).to_bytes(header,'big')
    client.sendall(msg_len+msg)


client=Client()                             #Creamos objeto de la clase cliente
    

    