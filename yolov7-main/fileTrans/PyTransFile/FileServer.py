import socket  # Import socket module
import time

import jpysocket
import threading

file_len = 0


def go():
    t1 = threading.Thread(target=str_server)
    t1.start()

    t2 = threading.Thread(target=file_server)
    t2.start()


def str_server():
    print('String Server Started')
    s = socket.socket()  # Create a socket object
    host = '127.0.0.1'  # Get local machine name
    port = 12345  # Reserve a port for your service.
    s.bind((host, port))  # Bind to the port
    s.listen(5)
    while True:
        conn, addr = s.accept()  # Establish connection with client.
        print("Got a string connection from", addr)
        t = threading.Thread(target=str_io, args=(conn,))
        t.start()


def str_io(conn):
    global file_len
    in_msg = conn.recv(1024);
    jpy_msg = jpysocket.jpydecode(in_msg)
    print(jpy_msg)
    # 這裏應該會收到一個 json string 裏面包含 檔案長度， 這裏直接傳檔案長度
    file_len = int(jpy_msg)
    out_msg = jpysocket.jpyencode("String from Server.")
    conn.send(out_msg)  # Send Msg
    conn.close()


def file_server():
    print('File Server Started')
    s = socket.socket()  # Create a socket object
    host = '127.0.0.1'  # Get local machine name
    port = 12350  # Reserve a port for your service.
    s.bind((host, port))  # Bind to the port
    s.listen(5)
    while True:
        print("Listening!")
        conn, addr = s.accept()  # Establish connection with client.
        print("Got a file connection from", addr)
        t = threading.Thread(target=file_io, args=(conn,))
        t.start()


def file_io(conn):
    receive_file(conn)
    send_file(conn)
    conn.close()


def receive_file(conn):
    global file_len
    f = open('image.jpg', 'wb')
    eof = bytes([0x00, 0x00, 0x00])
    total = 0
    while total < file_len:
        # print("receive")
        data = conn.recv(8192)
        f.write(data)
        total += len(data)
        # print(total)
    f.close()
    print("File Received!")


def send_file(conn):
    eof = bytes([0x00, 0x00, 0x00])
    f = open("image.jpg", "rb")
    data = f.read(8192)
    while data:
        conn.send(data)
        # print("send")
        data = f.read(8192)
    f.close()
    print("File Sent!")


if __name__ == '__main__':
    go()
