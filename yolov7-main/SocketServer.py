import socket
import threading
import sys
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
        # os.system('detect.py')
        print("from connected user: " + str(data))
        data = input('Hello, I am server!')
        # conn.send("Hello, I am server!")
        conn.send(data.encode())  # send data to the client

    conn.close()  # close the connection

def server_program():
    # get the hostname
    host = "120.110.113.213"
    port = 12345  # initiate port no above 1024

    # socket.AF_INET => 兩個server之間進行串接（這裡是client跟server感覺應該也可以用下面那個）
    # socket.AF_UNIX => 在本機端進行串接
    # socket.SOCK_STREAM => TCP宣告
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # bind用於server端要監聽的IP address跟Port
        server_socket.bind((host, port))  # bind host address and port together
    except socket.error as err:
        print("Bind failed")
        sys.exit()
    print("Socket bind success")

    server_socket.listen(2)  # 用於server端一次可接受多少socket串接
    print("Socket is now listening")

    while 1:
        conn, address = server_socket.accept()  # server端接收串接，並會回傳(client,address)串接對象與IP位址資訊
        print('Connect with ' + address[0] + ':' + str(address[1]))

        buf = conn.recv(64)
        print(buf)
        # conn.send("Hello, I am server!")
        t2 = threading.Thread(target=handle_client(conn, address))  # 建立新的執行緒
        t2.start()


if __name__ == '__main__':
    main()