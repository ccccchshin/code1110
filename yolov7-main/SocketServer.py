import socket
from io import BytesIO

import jpysocket
import threading
import sys
import json
import os
from PIL import Image


# 接收資料
def handle_client(conn):
    while 1:
        data = conn.recv(1024)  # String
        image = conn.recv(1024)
        # image 處理格式
        # handleImage = Image.open(BytesIO(image))
        # if not handleImage:
        #     print("Hello")
        msgrecv = jpysocket.jpydecode(data)
        if not msgrecv:
            # if data is not received break 檢查封包是否為空
            break
        print("keyword: " + msgrecv)

        os.system('detect.py')
        # detect.py have to catch 2 args image & keyword
        # os.popen() 把detect執行完的成果拿過來

        send_keyword(conn, msgrecv)
        # send image(conn, image)

        # print("from connected user: " + str(data))
        # get detect.py 執行過後的結果
        # return(detect.py傳過來的圖片)


# 送圖片
def send_image(conn, image):
    print("send_data", image)
    conn.send(image)


# 送文字
def send_keyword(conn, keyword):
    # data = data
    print("send_data", keyword)
    msgsend = jpysocket.jpyencode(keyword)  # Encript The Msg
    conn.send(msgsend)


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

    server_socket.listen(2)  # listen用於server端一次可接受多少socket串接
    print("Socket is now listening")

    while 1:
        conn, address = server_socket.accept()  # server端接收串接，並會回傳(client,address)串接對象與IP位址資訊
        print('Connect with ' + address[0] + ':' + str(address[1]))
        t1 = threading.Thread(target=handle_client(conn))
        t1.start()
        # conn.close()  # close the connection


def main():
    t = threading.Thread(target=server_program())  # 建立新的執行緒，讓執行緒去跑function
    t.start()


if __name__ == '__main__':
    main()
