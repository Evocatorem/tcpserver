import socket
import threading
import datetime
import sqlite3

bind_ip = '127.0.0.1'
bind_port = 9999
db_name = "users.db"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip, bind_port))
server.listen(5)  # max backlog of connections
journal = dict()
journal["admin"] = list()

print ('Listening on {}:{}'.format(bind_ip, bind_port))


def handle_client_connection(client_socket):
    # while(True):
    client_socket.send(bytes('Welcome to the server! Type signin, signup or exit', 'utf-8'))
    request = client_socket.recv(1024)
    if request == b'signin':
        client_socket.send(bytes('Enter you username', 'utf-8'))
        name = client_socket.recv(1024).decode('utf-8')
        data = read_db(name)
        print ('Received {}'.format(name))
        print(str(data))
        #print(name.decode('utf-8'))
        if name == 'admin':
            client_socket.send(bytes('Username ok, need password!', 'utf-8'))
            request = client_socket.recv(1024)
            if request == b'\x10\r\x10\xb0\x15':
                print("Login admin")
                journal["admin"].append(str(datetime.datetime.today())[0:-7])
                client_socket.send(bytes('Login successful', 'utf-8'))  
                client_socket.send(bytes(journal.__str__(), 'utf-8'))
        elif data:
            print("Connected %s" % name)
            client_socket.send(bytes('Username ok, need password!', 'utf-8'))
            request = client_socket.recv(1024)
            #print(str(request))
            print(data)
            if request in data:
                print("Login %s" % name)
                journal[name] = list()
                journal[name].append(str(datetime.datetime.today())[0:-7])
                client_socket.send(bytes('Login successful', 'utf-8'))
                client_socket.send(bytes("Welcome %s" % name, 'utf-8'))
            else:
                client_socket.send(bytes('Login failed', 'utf-8'))
                client_socket.close()

        else:
            client_socket.send(bytes('Username not found', 'utf-8'))
            client_socket.close()

    elif request == b'signup':
        client_socket.send(bytes('Your username:\n', 'utf-8'))
        name = client_socket.recv(1024).decode('utf-8')
        if read_db(name):
            print("User exist")
        print ('Received {}'.format(request.decode('utf-8')))
        client_socket.send(bytes('Your password:\n', 'utf-8'))
        passwd = client_socket.recv(1024)
        client_socket.send(bytes('Registration successful!\n', 'utf-8'))
        write_db(name, passwd)


def write_db(name, passwd):
    db = sqlite3.connect(db_name)
    db.execute('''INSERT INTO Top (NAME, PASS)
                VALUES (?,?)''', (name, passwd))
    db.commit()
    print("writed to db!", name, passwd)

def read_db(name):
    db = sqlite3.connect(db_name)
    c = db.cursor()
    try:
        c.execute(''' SELECT * FROM Top where NAME == "%s" ''' % name)
        print("Readed to db!")
        return c.fetchone()
    except:
        return None

while True:
    client_sock, address = server.accept()
    print ('Accepted connection from {}:{}'.format(address[0], address[1]))
    client_handler = threading.Thread(
        target=handle_client_connection,
        args=(client_sock,)  # without comma you'd get a... TypeError: handle_client_connection() argument after * must be a sequence, not _socketobject
    )
    client_handler.start()