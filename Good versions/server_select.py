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
        # self.writers=[]         #List of the objects that 
        self.add_readers(self.server)
        self.mobiles={}
        self.robots={}
        self.connections={}     #for now we will save all the client sockets with its own cient object

    def create_connection(self,mobile,robot):
        self.connections[mobile]=robot

    def add_readers(self,reader):
        self.readers.append(reader)
    
    def classify(self,obj):
        if obj.type=='ROBT':
            self.robots[obj.name]=obj
        if obj.type=='USER':
            self.mobiles[obj.name]=obj
        
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
                        self.connections[new_client.client]=new_client  #to remember the custom object related to the socket, we save it in a dictionary
                        print(f'New connection from {new_client.name}')
                    
                    #~~~~~~~~~~~~~~~~~~~~~~~  Client Block  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                    else:
                        msg=recv_msg(self.connections[reader])          #we call the global funtion tha allows recieve any msg
                        print(f'[{self.connections[reader].name}] {msg}')
                        if msg == '!DISCONNECT':                        #if the client dies, a !disconnect msg is recieved so we close and delete the client
                            reader.close()
                            self.readers.remove(reader)
                            del self.connections[reader]
                        if msg == '!LIST':
                            #s=''
                            print('Connected Mobiles:')
                            #s+='Connected Mobiles:\n'
                            for e in self.mobiles:
                                print(f' -{e}')
                                #s+=f' -{e}\n'
                            print('Connected Robots:')
                            #s+='Connected Robots:\n'
                            for e in self.robots:
                                print(f' -{e}')
                                #s+=f' -{e}\n'
                            #send_msg(s,reader)

        except KeyboardInterrupt:           #Protocol to desconect clients from server to leave the addres free
            print('Shutting down the server...')
            for reader in self.readers:
                reader.close()
                self.readers.remove(reader)
            sys.exit()


class Client():
    def __init__(self,sock,addr):
        self.client=sock
        self.data=b''
        self.name=''
        self.addr=addr
        self.type=''
    
    def set_name(self,name):
        self.type=name[:4]
        self.name=name[4:]
    
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
    client.sendall(msg_len+msg)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   Main Program   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    

server=Server()

        
    
    