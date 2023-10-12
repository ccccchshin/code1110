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
from PIL import Image

# global msgrecv
msgrecv = " "
# 接收字串
def handle_client(conn):
    print("hello I am handle_client")
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
        conn.send(data)
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
def send_image(conn, image):
    print("send_data", image)
    conn.send(image)


# 送文字
def send_keyword(conn, store_keyword):
    # data = data
    print("send_data", store_keyword)
    msgsend = jpysocket.jpyencode(store_keyword)  # Encript The Msg
    conn.send(msgsend)


# 接收圖片
def file_receive(conn):
    result = b''
    print("in file_receive")
    while True:
        print("in while")
        img = conn.recv(1024*20)  # 接收数据（适当调整缓冲区大小）
        print("after img")
        if not img:
            print("null qq")
            break
        print("result")
        result = result + img
    print("8181 while loop")
    with open('C:/Users/shin/410828608/yolov7-main/inference/image/app_image.jpg', 'wb') as file:
        file.write(result)
    print("Image received successfully")
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


def server_program():
    host = "120.110.113.213"  # get the hostname
    port = 12345  # initiate port no above 1024

    # socket.AF_INET => 兩個server之間進行串接（這裡是client跟server感覺應該也可以用下面那個但要問問看）
    # socket.AF_UNIX => 在本機端進行串接
    # socket.SOCK_STREAM => TCP宣告
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('socket created')

    try:
        server_socket.bind((host, port))  # bind用在server端要監聽的IP address跟Port
        print("Socket bind success")
    except socket.error as err:
        print("Bind failed")
        sys.exit()

    server_socket.listen(5)  # listen用於server端一次可接受多少socket串接
    print("Socket is now listening")

    while 1:
        conn, address = server_socket.accept()  # server端接收串接，並會回傳(client,address)串接對象與IP位址資訊
        print('Connect with ' + address[0] + ':' + str(address[1]))
        t1 = threading.Thread(target=handle_client, args=(conn,))
        # time.sleep(0.5)
        t1.start()
        print('socket call success')
        # conn.close()  # close the connection


def file_server():
    host = "120.110.113.213"  # get the hostname
    port = 12350  # initiate port no above 1024

    # socket.AF_INET => 兩個server之間進行串接（這裡是client跟server感覺應該也可以用下面那個但要問問看）
    # socket.AF_UNIX => 在本機端進行串接
    # socket.SOCK_STREAM => TCP宣告
    fserver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('fsocket created')

    try:
        fserver_socket.bind((host, port))  # bind用在server端要監聽的IP address跟Port
        print("fSocket bind success")
    except socket.error as err:
        print("fBind failed")
        sys.exit()

    fserver_socket.listen(5)  # listen用於server端一次可接受多少socket串接
    print("fSocket is now listening")

    while 1:
        conn, address = fserver_socket.accept()  # server端接收串接，並會回傳(client,address)串接對象與IP位址資訊
        print('Connect with ' + address[0] + ':' + str(address[1]))
        t1 = threading.Thread(target=file_receive, args=(conn,))
        t1.start()
        print('fsocket call success')
        # conn.close()  # close the connection


if __name__ == '__main__':

    str_thread = threading.Thread(target=server_program)
    img_thread = threading.Thread(target=file_server)
    print("check0")
    str_thread.start()
    img_thread.start()

