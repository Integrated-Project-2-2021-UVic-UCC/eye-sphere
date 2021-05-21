import socket
import sys
import select

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~   Classes   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Server():
    def __init__(self):
        self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.bind(('localhost',8080))
        self.sock.listen(10)
        self.sock.setblocking(False)

        self.event_loop=Event_loop(self.sock)
        print('Server Started!')
        self.event_loop.process_connections()   

class Event_loop():
    def __init__(self,server):
        self.server=server
        self.readers=[]         #List of the objects that has sent something to the server
        self.add_readers(self.server)
        self.mobiles=[]
        self.robots=[]
        self.clients_dic={}     #we save the custom client with it's socket obj. as the key to work easyly with select.
        self.connections={}     #tablished conections are saved here.

    def add_readers(self,reader):
        self.readers.append(reader)
    
    def classify(self,obj):
        if obj.type=='ROBT':
            self.robots.append(obj)
        if obj.type=='USER':
            self.mobiles.append(obj)
    
    def create_connection(self,mobile,robot):
        for r in self.robots:
            if r.name==robot:
                mobile.connected=True
                mobile.connect_client(r)
                r.connected=True
                r.connect_client(mobile)

    
    def detect_commands(self,msg,reader):

        if msg == '!DISCONNECT':                        #if the client dies, a !disconnect msg is recieved so we close and delete the client
            reader.close()
            dis_client=self.clients_dic[reader]
            if dis_client.type=='ROBT':
                self.robots.remove(dis_client)
                if dis_client.connected:
                    dis_client.connected_sock.connected=False
            if dis_client.type=='USER':
                self.mobiles.remove(dis_client)
                if dis_client.connected:
                    dis_client.connected_sock.connected=False

            self.readers.remove(reader)
            del self.clients_dic[reader]

        elif msg == '!LIST':                            #List commando
            s='Connected Mobiles:\n'
            for e in self.mobiles:
                s+=f' -{e.name}\n'
            s+='Connected Robots:\n'
            for e in self.robots:
                s+=f' -{e.name}\n'
            print(s)
            send_msg(s,self.clients_dic[reader])
        
        elif msg == '!CONNECT':                         #Connect command
            rob=recv_msg(self.clients_dic[reader])
            ok=0
            for obj in self.robots:
                if obj.name == rob:
                    send_msg(f'Connecting to {rob}',self.clients_dic[reader])
                    self.create_connection(self.clients_dic[reader],rob)
                    ok=1
            
            if ok == 0:
                send_msg(f'{rob} is not connected',self.clients_dic[reader])
        
    def process_connections(self):
        try:
            while True:
                readers, _, _=select.select(self.readers,[],[]) #wait until a new conection or a new message arrives
                for reader in readers:

                    #~~~~~~~~~~~~~~~~~~~~~~~  Server Block  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                    
                    if reader == self.server:                           #if the server is ready to read, means that a new connection arrives
                        conn, addr=self.server.accept()                 #the connection is accepted, and the socket object is returned
                        new_client=Client(conn,addr)                    #we save this connection in our custom class to take control of data sent
                        new_client.set_name(recv_msg(new_client))       #as the first msg from client is always the name, we save it
                        self.classify(new_client)
                        self.add_readers(new_client.client)             #we add the client socket object to the list of potencial readers
                        self.clients_dic[new_client.client]=new_client  #to remember the custom object related to the socket, we save it in a dictionary
                        print(f'New connection from {new_client.name}')
                    
                    #~~~~~~~~~~~~~~~~~~~~~~~  Client Block  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                    else:
                        if self.clients_dic[reader].connected:
                            msg=recv_msg(self.clients_dic[reader])          #we call the global funtion tha allows recieve any msg
                            send_msg(msg,self.clients_dic[reader].connected_sock)
                            print('connect message')
                        else:
                            msg=recv_msg(self.clients_dic[reader])          #we call the global funtion tha allows recieve any msg
                        print(f'[{self.clients_dic[reader].name}] {msg}')
                        self.detect_commands(msg,reader)


        except KeyboardInterrupt:           #Protocol to desconect clients from server to leave the addres free
            print('Shutting down the server...')
            for reader in self.readers:
                reader.close()
                self.readers.remove(reader)
            sys.exit()


class Client():
    def __init__(self,sock,addr):
        self.client=sock
        self.connected=False
        self.data=b''
        self.name=''
        self.addr=addr
        self.type=''
        self.connected_sock=''
    
    def set_name(self,name):
        self.type=name[:4]
        self.name=name[4:]
    
    def connect_client(self,obj):
        self.connected_sock=obj
    
    def build_data(self,data):
        self.data+=data

    def save_data(self,data):
        self.data=data
    
    def get_data(self):
        return self.data

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   Global funtions   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def recv_msg(client):
    header_size=6
    while len(client.get_data())<header_size:
        client.build_data(client.client.recv(header_size))
    
    header=client.get_data()[:header_size]
    client.save_data(client.get_data()[header_size:])
    data_size=int.from_bytes(header,'big')

    while len(client.get_data()) < data_size:
        client.build_data(client.client.recv(data_size))
    
    final_data=client.get_data()[:data_size].decode('utf8')
    client.save_data(client.get_data()[data_size:])
    return final_data

def send_msg(msg,client):
    header=6
    msg=msg.encode('utf8')
    msg_len=len(msg).to_bytes(header,'big')
    client.client.sendall(msg_len+msg)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   Main Program   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    

server=Server()

        
    
    