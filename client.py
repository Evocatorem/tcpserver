#V7 212 323 199 342 211

import socket
import math


def main():

    # # create an ipv4 (AF_INET) socket object using the tcp protocol (SOCK_STREAM)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #
    # # connect the client
    #client.connect((target, port))
    client.connect(('127.0.0.1', 9999))
    response = client.recv(4096)
    print(response.decode('utf-8'))
    command = input("Command:\n")
    client.send(bytes(command, 'utf-8'))
    response = client.recv(4096)
    print(response.decode('utf-8'))
    # send some data
    #client.send(bytes("lol", 'utf-8'))
    if command == "signin":
        client.send(bytes(input(),'utf-8'))
        response = client.recv(4096)
        if response == b'Username ok, need password!':
            client.send(encrypt())
        else:
            exit(0)
        response = client.recv(4096)
        print(response)
        if response == b'Login successful':
            response = client.recv(4096)
            print(response.decode('utf-8'))
            client.close()
    elif command == "signup":
        client.send(bytes(input("\n"), 'utf-8'))
        response = client.recv(4096)
        print(response.decode('utf-8'))
        client.send(encrypt())
        response = client.recv(4096)
        print(response.decode('utf-8'))
        client.close()
    elif command == "exit":
        client.close()
    # receive the response data (4096 is recommended buffer size)




def encrypt():
    encrypt = list()
    passwd = input("Pass:\n")
    passwd = bytearray(passwd, 'utf-8')
    for x in passwd:
        encrypt.append(int((math.pow(x, 7) + 212 * math.pow(x, 6) + 323 * math.pow(x, 5) + 199 * x + 342) % 211))
    print(bytes(encrypt))
    return bytes(encrypt)

if __name__ == '__main__':
    main()