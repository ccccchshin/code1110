import socket
import threading

import os

def main():
    t = threading.Thread(target=server_program()) # 建立新的執行緒
    t.start();
    # t2 = threading.Thread(target=....)


def handle_client(conn, addr):
    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(1024).decode()  # get到封包並解析
        if not data:
            # if data is not received break 檢查封包是否為空
            break
        os.system('detect.py')

        print("from connected user: " + str(data))
        data = input(' -> ')
        conn.send(data.encode())  # send data to the client

    conn.close()  # close the connection

def server_program():
    # get the hostname
    host = socket.gethostname()
    port = 5000  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(2) # 看server一次可以監聽有多少個client
    conn, address = server_socket.accept()  # accept new connection
    t3 = threading.Thread(target=handle_client(conn, address)) # 建立新的執行緒
    print("Connection from: " + str(address))

if __name__ == '__main__':
    main()