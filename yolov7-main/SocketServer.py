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
        # if not msgrecv:
        #     # if data is not received break 檢查封包是否為空
        #     print("no get string data")
        #     # time.sleep(0.5)
        #     break
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
    try:
        while 1:
        # image 處理格式
            image = conn.recv(1024)  # image
            image_arr = bytearray()

            image_arr.extend(image)

            # if len(image_arr) == 0:
            #     print("img null or not?")
            # #    break
            if result_image is not None:
                    cv2.imshow('app_image.JPG', result_image)

                    print("img get failed3")
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()
                    print("get owari")
            else:
                print("失敗")

            print("img get over")
            # result_image = np.ascontiguousarray(bytearray(image_arr), dtype="uint8")

            # result_image = cv2.imdecode(result_image, cv2.IMREAD_COLOR)
            result_image = cv2.imdecode(np.ascontiguousarray(bytearray(image_arr), dtype="uint8"), cv2.IMREAD_COLOR)

            print("img get failed0")

                # result_image = cv2.imread('C:/Users/shin/410828608/yolov7-main/inference/images/app_image.JPG',0)
                # result_image = cv2.imdecode(result_image, cv2.IMREAD_COLOR)
                # print("img get failed1")
                # count = 0
                #寫入並儲存圖片
                # cv2.imwrite('C:/Users/shin/410828608/yolov7-main/inference/images/app_image'+str(count)+'.JPG', result_image)
                # tempPath = 'C:/Users/shin/410828608/yolov7-main/inference/images/app_image'+str(count)+'.JPG'
                # count = count + 1
                # print("img get failed2")

                # result_image = cv2.imread(tempPath, 0)

        # while True:
        #     data = conn.recv(1024)
        #     # print('data, ', data)
        #     if not data or len(data) == 0:
        #         print("no")
        #         break
        # conn.close()
    except Exception:
        print("connect bye")


class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        print("get.....")
        image1 = []
        try:
            while True:
                data = self.request.recv(1024)
                print('data, ', data)
                if not data or len(data) == 0:
                    print("no")
                    break
                image1.extend(data)
            print("get over")
            image = np.asarray(bytearray(image1), dtype="uint8")
            image = cv2.imdecord(image, cv2.IMREAD_COLOR)
            cv2.namedWindow("Image")
            cv2.imshow("Image", image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            print("get owari")
            self.request.sendall("get ur connect!".encode("utf-8"))
        except Exception:
            print(self.client_address, "connect bye")
        finally:
            self.request.close()

    # def setup(self):
    #     now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #     print(now_time)
    #     print("connect build: ", self.client_address)
    #
    # def finish(self):
    #     print("connect free")


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
        # time.sleep(0.5)
        # conn.close()  # close the connection


# def main():
#     t = threading.Thread(target=server_program())  # 建立新的執行緒，讓執行緒去跑function
#     t2 = threading.Thread(target=file_server())
#     t.start()
#     print("check")
#     t2.start()

    # img_server = socketserver.ThreadingTCPServer(("120.110.113.213", 12350), MyTCPHandler)
    # print("run yes")
    # img_server.serve_forever()
    # t_image = threading.Thread(target=image_server())  # 建立新的執行緒，讓執行緒去跑function
    # t_image.start()


if __name__ == '__main__':

    str_thread = threading.Thread(target=server_program)
    img_thread = threading.Thread(target=file_server)
    print("check0")
    str_thread.start()
    img_thread.start()

