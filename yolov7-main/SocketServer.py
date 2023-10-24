import socket
import detect
# import module
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

# global msgrecv
msgrecv = " "
file_len = 0

# str ------------------------------------------------------------------------str

# def init_keyword(keyword):
#     keyword = msgrecv
#     return keyword

def str_io(conn):
    global msgrecv
    # msgrecv = ""
    while True:
        # 字串處理
        data = conn.recv(1024)  # String
        msgrecv = jpysocket.jpydecode(data)
        if not msgrecv:
        #     # if data is not received break 檢查封包是否為空
        #     print("no get string data")
        #     # time.sleep(0.5)
            break
        print("keyword: " + msgrecv)
        out_msg = jpysocket.jpyencode("keyword: " + msgrecv)
        conn.send(out_msg)
        # conn.sendall(msgrecv.encode("utf-8"))
        # conn.sendall("OK".encode("utf-8"))
        print("get ok")

    print("conn 8181")
    conn.close()

        # os.system('detect.py')
        # detect.py have to catch 2 args image & keyword
        # os.popen() 把detect執行完的成果拿過來

        # send_keyword(conn, msgrecv) yy
        # send image(conn, image)

        # print("from connected user: " + str(data))
        # get detect.py 執行過後的結果
        # return(detect.py傳過來的圖片)


def str_server():
    host = "120.110.113.213"  # get the hostname
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
        t1 = threading.Thread(target=str_io, args=(conn,))
        t1.start()
        print('str socket call success')


# def get_image(conn):
#
#     while 1:
#         # image 處理格式
#         image = conn.recv(1024)  # image
#         image_arr = []
#         image_arr.extend(image)
#
#         if len(image_arr) == 0:
#             print("null or not?")
#         #     break
#
#         print("get over")
#         result_image = np.ascontiguousarray(bytearray(image_arr), dtype="uint8")
#
#         result_image = cv2.imdecode(result_image, cv2.IMREAD_COLOR)
#
#         cv2.namedWindow("Image")
#         cv2.imshow("Image", result_image)
#         cv2.waitKey(0)
#         cv2.destroyAllWindows()
#
#         print("get owari")


# 送圖片
# def send_image(conn, image):
#     print("send_data", image)
#     conn.send(image)

# 送文字
# def send_keyword(conn, store_keyword):
#     # data = data
#     print("send_data", store_keyword)
#     msgsend = jpysocket.jpyencode(store_keyword)  # Encript The Msg
#     conn.send(msgsend)

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
    host = "120.110.113.213"  # get the hostname
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
        t1 = threading.Thread(target=len_io, args=(conn,))
        t1.start()
        print('len socket call success')


# file ------------------------------------------------------------------------------- file

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


    # result = b''
    # print("in file_receive")
    # while True:
    #     print("in while")
    #     img = conn.recv(1024*20)  # 接收数据（适当调整缓冲区大小）
    #     print("after img")
    #     if not img:
    #         print("null qq")
    #         break
    #     print("result")
    #     result = result + img
    # print("8181 while loop")
    # with open('C:/Users/shin/410828608/yolov7-main/inference/image/app_image.jpg', 'wb') as file:
    #     file.write(result)
    # print("Image received successfully")
    # try:
    #     rec_img = b''
    #     # rec_img = bytes([])
    #     while 1:
    #         # image 處理格式
    #         image = conn.recv(1024*10)  # image
    #         # image_arr = bytearray()
    #         # all_img = bytearray.append(image_arr)
    #         # image_arr.extend(image)
    #
    #         if not image:
    #             print("img null")
    #             break
    #         rec_img = rec_img + base64.b64decode(image)
    #             #         cv2.imshow('app_image.JPG', result_image)
    #             #
    #             #         print("img get failed3")
    #             #         cv2.waitKey(0)
    #             #         cv2.destroyAllWindows()
    #             #         print("get owari")
    #             # else:
    #             #     print("失敗")
    #
    #             # if not image or len(image) == 0:
    #             #     print("img null or not?")
    #             #     break
    #             # else:
    #             #     rec_img = rec_img + image
    #         # if result_image is not None:
    #         #         cv2.imshow('app_image.JPG', result_image)
    #         #
    #         #         print("img get failed3")
    #         #         cv2.waitKey(0)
    #         #         cv2.destroyAllWindows()
    #         #         print("get owari")
    #         # else:
    #         #     print("失敗")
    #         #
    #         # print("img get over")
    #         # # result_image = np.ascontiguousarray(bytearray(image_arr), dtype="uint8")
    #         #
    #         # # result_image = cv2.imdecode(result_image, cv2.IMREAD_COLOR)
    #         # result_image = cv2.imdecode(np.ascontiguousarray(bytearray(image_arr), dtype="uint8"), cv2.IMREAD_COLOR)
    #         #
    #         # print("img get failed0")
    #         #
    #         #     # result_image = cv2.imread('C:/Users/shin/410828608/yolov7-main/inference/images/app_image.JPG',0)
    #         #     # result_image = cv2.imdecode(result_image, cv2.IMREAD_COLOR)
    #         #     # print("img get failed1")
    #         #     # count = 0
    #         #     #寫入並儲存圖片
    #         #     # cv2.imwrite('C:/Users/shin/410828608/yolov7-main/inference/images/app_image'+str(count)+'.JPG', result_image)
    #         #     # tempPath = 'C:/Users/shin/410828608/yolov7-main/inference/images/app_image'+str(count)+'.JPG'
    #         #     # count = count + 1
    #         #     # print("img get failed2")
    #         #
    #         #     # result_image = cv2.imread(tempPath, 0)
    #     print(len(rec_img))
    #     # if rec_img:
    #     if len(rec_img) > 0:
    #
    #         np_arr = np.fromstring(rec_img, np.uint8)
    #         result_image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    #         cv2.imshow('Received Image', result_image)
    #         cv2.waitKey(0)
    #         cv2.destroyAllWindows()
    #         conn.send("Image received".encode())
    #     else:
    #         conn.send("No image received".encode())
    #     # print("get over1012")
    #     # rec_img = base64.b64decode(rec_img)
    #     # np_arr = np.frombuffer(rec_img, np.uint8)
    #     # result = cv2.imdecode(np_arr, 1)
    #     # cv2.imshow('image', result)
    #     # cv2.waitKey(0)
    #     # cv2.destroyAllWindows()
    #     # conn.send("111".encode())
    #
    # except Exception as e:
    #     print("Error:", e)
    #     print("connect bye")
    # finally:
    #     conn.close()


def send_file(conn):
    eof = bytes([0x00, 0x00, 0x00])
    print("test1")
    f = open("C:/Users/shin/410828608/yolov7-main/image.jpg", "rb+")
    print("test2")
    data = f.read(8192)
    print("test3")
    try:
        while data:
            print("test4")
            conn.send(data)
            print("send")
            data = f.read(8192)
    except Exception as e:
        print(e)
    f.close()
    print("File Sent!")


def file_io(conn):
    receive_file(conn)
    print("receive_file")
    # os.system('detect.py')
    # os.system('ServerTest.py')
    # detect()
    # python_script_path = 'detect.py'
    # script_args = ['C:/Users/shin/410828608/yolov7-main/image.jpg',
    #                'C:/Users/shin/runs/train/exp14/weights/best.pt']
    send_file(conn)
    print("send_file")
    conn.close()


def file_server():
    host = "120.110.113.213"  # get the hostname
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
        t1 = threading.Thread(target=file_io, args=(conn,))
        t1.start()
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


