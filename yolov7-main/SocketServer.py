# -*- coding: utf-8 -*-
import socket

import time

import jpysocket
import threading

import subprocess


global msgrecv
msgrecv = '11'

file_len = 0
str_len = 0
msgrecv_lock = threading.Lock()


# str ------------------------------------------------------------------------ str

def str_io(conn):
    temp = ''
    # 字串處理
    data = conn.recv(8192)  # String
    temp = temp + jpysocket.jpydecode(data)
    if not data:
        print("not string data")
    with msgrecv_lock:
        msgrecv = temp

    erase_txt(1)

    file_path = "C:/Users/User/410828608/yolov7-main/store_keyword.txt"  # 指定文件的路徑
    with open(file_path, "a") as file:
        new_contents = msgrecv
        file.write(new_contents)
    print("已被覆蓋")

    print("keyword: " + msgrecv)
    # time.sleep(1)
    out_msg = jpysocket.jpyencode("ok")

    conn.send(out_msg)

    data = conn.recv(8192)  # String
    temp = temp + jpysocket.jpydecode(data)

    print("get ack")
    print("conn 8181")
    # conn.close()


def erase_txt(mode):
    if mode == 1:
        file_path = "C:/Users/User/410828608/yolov7-main/store_keyword.txt"  # 指定文件的路徑
        with open(file_path, "w") as file:
            print('文件內容已清除')
    elif mode == 2:
        file_path = "C:/Users/User/410828608/yolov7-main/chat_ocr.txt"  # 指定文件的路徑
        with open(file_path, "w") as file:
            print('文件內容已清除')


def str_server():
    host = "120.110.113.204"  # get the hostname
    port = 12345  # initiate port no above 1024

    # socket.AF_INET => 兩個server之間進行串接（這裡是client跟server感覺應該也可以用下面那個但要問問看）
    # socket.AF_UNIX => 在本機端進行串接
    # socket.SOCK_STREAM => TCP宣告
    str_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('str socket created')
    str_socket.bind((host, port))
    print("str socket bind success")
    str_socket.listen(5)  # listen用於server端一次可接受多少socket串接
    print("str socket is now listening")

    while True:
        conn, address = str_socket.accept()  # server端接收串接，並會回傳(client,address)串接對象與IP位址資訊
        print('Connect with ' + address[0] + ':' + str(address[1]))
        str_io(conn)
        print('str socket call success')
        time.sleep(1)
        conn.close()


# len ------------------------------------------------------------------------------ len

def len_io(conn, mode):
    global file_len
    in_msg = conn.recv(1024)
    jpy_msg = jpysocket.jpydecode(in_msg)
    print(jpy_msg)
    # 這裏應該會收到一個 json string 裏面包含 檔案長度， 這裏直接傳檔案長度
    file_len = int(jpy_msg)
    out_msg = jpysocket.jpyencode("len from Server.")
    conn.send(out_msg)  # Send Msg
    if mode == 1:
        print("Mode 1 over")
    elif mode == 2:
        print("Mode 2 over")
    conn.close()

def len_server():
    host = "120.110.113.204"  # get the hostname
    port = 12355  # initiate port no above 1024

    # socket.AF_INET => 兩個server之間進行串接（這裡是client跟server感覺應該也可以用下面那個但要問問看）
    # socket.AF_UNIX => 在本機端進行串接
    # socket.SOCK_STREAM => TCP宣告
    str_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('len socket created')
    str_socket.bind((host, port))
    print("len socket bind success")
    str_socket.listen(5)  # listen用於server端一次可接受多少socket串接
    print("len socket is now listening")

    while True:
        conn, address = str_socket.accept()  # server端接收串接，並會回傳(client,address)串接對象與IP位址資訊
        print('Connect with ' + address[0] + ':' + str(address[1]))
        len_io(conn, 1)
        print('len socket call success')


# file ------------------------------------------------------------------------------- file

def send_file(conn):
    eof = bytes([0x00, 0x00, 0x00])
    f = open("C:/Users/User/410828608/yolov7-main/draw_result.jpg", "rb+")
    data = f.read(8192)
    try:
        while data:
            conn.send(data)
            data = f.read(8192)
    except Exception as e:
        print(e)
    f.close()
    print("File Sent!")


def file_io(conn):
    receive_file(conn, 1)
    print("receive_file")
    subprocess.run(['python', 'detect.py'], text=True)
    erase_txt(1)
    send_file(conn)
    print("send_file")
    conn.close()


def receive_file(conn, mode):
    global file_len
    total = 0

    if mode == 1:
        f = open('image.jpg', 'wb+')
        while total < file_len:
            data = conn.recv(8192)
            f.write(data)
            total += len(data)
        print("File Received!")
    elif mode == 2:
        f = open('chat_ocr.JPG', 'wb+')
        while total < file_len:
            data = conn.recv(8192)
            f.write(data)
            total += len(data)
        print("chat_ocr File Received!")
    f.close()


def file_server():
    host = "120.110.113.204"  # get the hostname
    port = 12350  # initiate port no above 1024
    # socket.AF_INET => 兩個server之間進行串接（這裡是client跟server感覺應該也可以用下面那個但要問問看）
    # socket.AF_UNIX => 在本機端進行串接
    # socket.SOCK_STREAM => TCP宣告
    file_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('file socket created')
    file_socket.bind((host, port))
    print("file socket bind success")
    file_socket.listen(5)  # listen用於server端一次可接受多少socket串接
    print("file socket is now listening")

    while True:
        conn, address = file_socket.accept()  # server端接收串接，並會回傳(client,address)串接對象與IP位址資訊
        print('Connect with ' + address[0] + ':' + str(address[1]))
        file_io(conn)
        print('file socket call success')

# chat_ocr ------------------------------------------------------------------------------- chat_ocr


def ocr_len_server():
    host = "120.110.113.204"  # get the hostname
    port = 12370  # initiate port no above 1024

    # socket.AF_INET => 兩個server之間進行串接（這裡是client跟server感覺應該也可以用下面那個但要問問看）
    # socket.AF_UNIX => 在本機端進行串接
    # socket.SOCK_STREAM => TCP宣告
    ocr_len_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('ocr_len socket created')
    ocr_len_socket.bind((host, port))
    print("ocr_len socket bind success")
    ocr_len_socket.listen(5)  # listen用於server端一次可接受多少socket串接
    print("ocr_len socket is now listening")

    while True:
        conn, address = ocr_len_socket.accept()  # server端接收串接，並會回傳(client,address)串接對象與IP位址資訊
        print('Connect with ' + address[0] + ':' + str(address[1]))
        len_io(conn, 2)
        print('ocr_len socket call success')


def send_ocr_string(conn):
    f = open("C:/Users/User/410828608/yolov7-main/chat_ocr.txt", "rb+")
    data = f.read(8192)
    try:
        while data:
            conn.send(data)

            data = f.read(8192)
    except Exception as e:
        print(e)
    f.close()
    erase_txt(2)
    print("chat_ocr_result Sent!")


def rec_ocr_io(conn):
    receive_file(conn, 2)
    print("receive_file")
    subprocess.run(['python', 'Chat_ocr.py'], text=True)
    send_ocr_string(conn)
    conn.close()


def ocr_rec_server():
    host = "120.110.113.204"
    port = 12365

    ocr_rec_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('rec_ocr_socket created')
    ocr_rec_socket.bind((host, port))
    print("rec_ocr_socket bind success")
    ocr_rec_socket.listen(5)  # listen用於server端一次可接受多少socket串接
    print("rec_ocr_socket is now listening")

    while True:
        conn, address = ocr_rec_socket.accept()  # server端接收串接，並會回傳(client,address)串接對象與IP位址資訊
        print('Connect with ' + address[0] + ':' + str(address[1]))
        rec_ocr_io(conn)
        print('rec_ocr_socket call success')


def go():
    str_thread = threading.Thread(target=str_server)
    len_thread = threading.Thread(target=len_server)
    img_thread = threading.Thread(target=file_server)
    ocr_rec_thread = threading.Thread(target=ocr_rec_server)
    ocr_len_thread = threading.Thread(target=ocr_len_server)
    print("check0")
    str_thread.start()
    len_thread.start()
    img_thread.start()
    ocr_rec_thread.start()
    ocr_len_thread.start()


if __name__ == '__main__':
    go()
