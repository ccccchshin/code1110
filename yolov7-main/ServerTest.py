import threading
import time


def aa():
    i = 0
    while i < 5:
        i = i + 1
        time.sleep(0.5)
        print('A:', i)


def bb():
    i = 0
    while i < 50:
        i = i + 10
        time.sleep(0.5)
        print('B:', i)


if __name__ == '__main__':
    a = threading.Thread(target=aa)
    print("hello aa")
    b = threading.Thread(target=bb)
    print("hello bb")
    a.start()
    b.start()


# import socket
# import sys
#
# HOST = "120.110.113.213"
# PORT = 12345
#
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# print('socket created')
#
# # Bind socket to Host and Port
# try:
#     s.bind((HOST, PORT))
# except socket.error as err:
#     print("Bind Failed")
#     sys.exit()
#
# print("Socket Bind Success!")
#
# # listen(): This method sets up and start TCP listener.
# s.listen(10)
# print("Socket is now listening")
#
# while 1:
#     conn, addr = s.accept()
#     print('Connect with ' + addr[0] + ':' + str(addr[1]))
#     buf = conn.recv(64)
#     print(buf)
# s.close()
#
# # import socket               # Import socket module
# #
# # soc = socket.socket()         # Create a socket object
# # host = "localhost"         # Get local machine name
# # port = 2004                # Reserve a port for your service.
# # soc.bind((host, port))       # Bind to the port
# # soc.listen(5)                 # Now wait for client connection.
# # while True:
# #     conn, addr = soc.accept()     # Establish connection with client.
# #     print('Got connection from', addr)
# #     msg = conn.recv(1024)
# #     print(msg)
# #     if msg == "Hello Server":
# #         print("Hii everyone")
# #     else:
# #         print("Go away")
