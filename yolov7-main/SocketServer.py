# -*- coding: utf-8 -*-

import socket
import socketserver
import time
import numpy as np
import cv2
import base64

import jpysocket
import threading
import sys
import json
import os
import subprocess
from PIL import Image

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
        #     # if data is not received break 檢查封包是否為空
        #     print("no get string data")
        #     # time.sleep(0.5)
        print("not string data")
    with msgrecv_lock:
        msgrecv = temp

    erase_txt()

    file_path = "C:/Users/shin/410828608/yolov7-main/store_keyword.txt"  # 指定文件的路徑
    with open(file_path, "a") as file:
        new_contents = msgrecv
        file.write(new_contents)
    print("已被覆蓋")

    print("keyword: " + msgrecv)
    # time.sleep(1)
    out_msg = jpysocket.jpyencode("ok")

    conn.send(out_msg)
    # time.sleep(1)
    # conn.sendall(msgrecv.encode("utf-8"))
    # conn.sendall("OK".encode("utf-8"))

    data = conn.recv(8192)  # String
    temp = temp + jpysocket.jpydecode(data)

    print("get ack")

    print("conn 8181")
    # conn.close()


def erase_txt():
    file_path = "C:/Users/shin/410828608/yolov7-main/store_keyword.txt"  # 指定文件的路徑
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

def len_io(conn):
    global file_len
    in_msg = conn.recv(1024)
    jpy_msg = jpysocket.jpydecode(in_msg)
    print(jpy_msg)
    # 這裏應該會收到一個 json string 裏面包含 檔案長度， 這裏直接傳檔案長度
    file_len = int(jpy_msg)
    out_msg = jpysocket.jpyencode("len from Server.")
    conn.send(out_msg)  # Send Msg
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
        len_io(conn)
        print('len socket call success')


# file ------------------------------------------------------------------------------- file

def send_file(conn):
    eof = bytes([0x00, 0x00, 0x00])
    f = open("C:/Users/shin/410828608/yolov7-main/draw_result.jpg", "rb+")
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
    receive_file(conn)
    print("receive_file")
    subprocess.run(['python', 'detect.py'], text=True)
    erase_txt()
    send_file(conn)
    print("send_file")
    conn.close()


def receive_file(conn):
    global file_len
    f = open('image.jpg', 'wb+')
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


def go():
    str_thread = threading.Thread(target=str_server)
    len_thread = threading.Thread(target=len_server)
    img_thread = threading.Thread(target=file_server)
    print("check0")
    str_thread.start()
    len_thread.start()
    img_thread.start()


if __name__ == '__main__':
    go()
