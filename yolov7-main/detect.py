# -*- coding: utf-8 -*-

import argparse
import operator
import sys

# import ServerTest
import socket
import SocketServer as soc
import time
from pathlib import Path
# from ServerTest import msgrecv

import cv2
import torch
import torch.backends.cudnn as cudnn
from numpy import random

#####
from imageio.plugins import opencv
from paddleocr import PaddleOCR
from matplotlib import pyplot as plt
import os
#####

import numpy as np

from models.experimental import attempt_load
from utils.datasets import LoadStreams, LoadImages
from utils.general import check_img_size, check_requirements, check_imshow, non_max_suppression, apply_classifier, \
    scale_coords, xyxy2xywh, strip_optimizer, set_logging, increment_path
from utils.plots import plot_one_box
from utils.torch_utils import select_device, load_classifier, time_synchronized, TracedModel

ser_keyword = ""


#
# import pytesseract
# from PIL import Image
#

# 獲取相對應的參數和測試(判斷測試是本地圖片還是網路圖片)

def detect(save_img=False):
    source, weights, view_img, save_txt, imgsz, trace = opt.source, opt.weights, opt.view_img, opt.save_txt, opt.img_size, not opt.no_trace
    save_img = not opt.nosave and not source.endswith('.txt')  # save inference images
    webcam = source.isnumeric() or source.endswith('.txt') or source.lower().startswith(
        ('rtsp://', 'rtmp://', 'http://', 'https://'))

    # Directories
    # 建立保存訓練結果的資料夾
    save_dir = Path(increment_path(Path(opt.project) / opt.name, exist_ok=opt.exist_ok))  # increment run
    (save_dir / 'labels' if save_txt else save_dir).mkdir(parents=True, exist_ok=True)  # make dir

    # Initialize
    # 選擇使用 cpu 還是 cuda 進行測試
    set_logging()
    device = select_device(opt.device)
    # half = device.type != 'cpu'  # half precision only supported on CUDA
    half = False

    # Load model
    # 加載權重文件 (if沒上傳自己的權重文件，會自動下載預先訓練好的模型權重文件)
    model = attempt_load(weights, map_location=device)  # load FP32 model

    # 檢測圖片大小, if測試圖片不是 32 的倍數, 那麼會自動調整為 32 的倍數 (調用 make_divisible 方法)
    stride = int(model.stride.max())  # model stride
    imgsz = check_img_size(imgsz, s=stride)  # check img_size

    # 判斷是否進行 libtorch 轉換和參數 half 操作
    if trace:
        model = TracedModel(model, device, opt.img_size)
    if half:
        model.half()  # to FP16

    # Second-stage classifier
    # 看user是否選擇用一個分類網絡來對定位的內容進行分類
    classify = False
    if classify:
        modelc = load_classifier(name='resnet101', n=2)  # initialize
        modelc.load_state_dict(torch.load('weights/resnet101.pt', map_location=device)['model']).to(device).eval()

    # Set Dataloader
    vid_path, vid_writer = None, None
    if webcam:
        view_img = check_imshow()
        cudnn.benchmark = True  # set True to speed up constant image size inference
        dataset = LoadStreams(source, img_size=imgsz, stride=stride)
        # 待預測圖片路徑, 網絡支持的預測圖片大小, 網絡的最大步長
    else:
        dataset = LoadImages(source, img_size=imgsz, stride=stride)

    # Get names and colors
    names = model.module.names if hasattr(model, 'module') else model.names
    colors = [[random.randint(0, 255) for _ in range(3)] for _ in names]

    # Run inference
    # 對圖片進行歸一化操作
    if device.type != 'cpu':
        model(torch.zeros(1, 3, imgsz, imgsz).to(device).type_as(next(model.parameters())))  # run once
    old_img_w = old_img_h = imgsz
    old_img_b = 1

    t0 = time.time()
    for path, img, im0s, vid_cap in dataset:
        img = torch.from_numpy(img).to(device)
        img = img.half() if half else img.float()  # uint8 to fp16/32
        img /= 255.0  # 0 - 255 to 0.0 - 1.0

        # img.ndimension() 返回tensor對象的維度
        # img.unsqueeze(0) 在指定維度上添加一個維度
        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        # Warmup
        if device.type != 'cpu' and (
                old_img_b != img.shape[0] or old_img_h != img.shape[2] or old_img_w != img.shape[3]):
            old_img_b = img.shape[0]
            old_img_h = img.shape[2]
            old_img_w = img.shape[3]
            for i in range(3):
                model(img, augment=opt.augment)[0]

        # Inference
        # 將測試圖片餵入網絡中, 得到預測結果 (有可能會預測出來很多框, 後續會再使用nms的方法去移除多餘的框)
        t1 = time_synchronized()
        pred = model(img, augment=opt.augment)[0]
        t2 = time_synchronized()

        # Apply NMS
        # 對預測結果進行nms的操作 (去除多餘的框)
        pred = non_max_suppression(pred, opt.conf_thres, opt.iou_thres, classes=opt.classes, agnostic=opt.agnostic_nms)
        t3 = time_synchronized()

        # Apply Classifier
        if classify:
            pred = apply_classifier(pred, modelc, img, im0s)

        # Process detections
        # 針對每一張待預測圖片, 遍歷輸出結果, 創建相對應的保存路徑
        # gn 表示經過resize之後的長寬 (方便後續xyxy2xywh的操作)

        for i, det in enumerate(pred):  # detections per image
            if webcam:  # batch_size >= 1
                p, s, im0, frame = path[i], '%g: ' % i, im0s[i].copy(), dataset.count
            else:
                p, s, im0, frame = path, '', im0s, getattr(dataset, 'frame', 0)

            p = Path(p)  # to Path
            save_path = str(save_dir / p.name)  # img.jpg
            txt_path = str(save_dir / 'labels' / p.stem) + ('' if dataset.mode == 'image' else f'_{frame}')  # img.txt
            gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh

            # scale_coords 將預測的結果進行轉換, 因為我們剛剛有使用 gn 進行resize的處理
            # 因此要依照剛剛調整的比例將預測的框對應到原本圖片的大小
            if len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()

                # Print results
                for c in det[:, -1].unique():
                    n = (det[:, -1] == c).sum()  # detections per class
                    s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # add to string

                # Write results
                imgNo = 0
                for *xyxy, conf, cls in reversed(det):
                    if save_txt:  # Write to file
                        xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(-1).tolist()  # normalized xywh
                        line = (cls, *xywh, conf) if opt.save_conf else (cls, *xywh)  # label format
                        with open(txt_path + '.txt', 'a') as f:
                            f.write(('%g ' * len(line)).rstrip() % line + '\n')

                    if save_img or view_img:  # Add bbox to image
                        label = f'{names[int(cls)]} {conf:.2f}'
                        plot_one_box(xyxy, im0, label=label, color=colors[int(cls)], line_thickness=1)

                    if names[int(cls)] == 'nutrition':
                        f_name = save_path.split(".")[0]
                        # print('i am f_name: ' + f_name)
                        crop_image(xyxy, im0, imgNo, f_name)
                        imgNo = imgNo + 1

            else:
                img_num = 0
                f_name = save_path.split(".")[0]
                no_crop(im0, img_num, f_name)


            # Print time (inference + NMS)
            print(f'{s}Done. ({(1E3 * (t2 - t1)):.1f}ms) Inference, ({(1E3 * (t3 - t2)):.1f}ms) NMS')
            # 我選取到的範圍都print出來
            # test_arg = np.array(scale_coords(img.shape[2:], det[:, :4], im0.shape).round())
            # print("一般座標：" + test_arg)
            # print("tensor：" + scale_coords(img.shape[2:], det[:, :4], im0.shape).round())

            # Stream results
            if view_img:
                cv2.imshow(str(p), im0)
                cv2.waitKey(1)  # 1 millisecond
                ###
                cap = cv2.VideoCapture(0)

            # Save results (image with detections)
            if save_img:
                if dataset.mode == 'image':
                    cv2.imwrite(save_path, im0)
                    print(f" The image with the result is saved in: {save_path}")
                else:  # 'video' or 'stream'
                    if vid_path != save_path:  # new video
                        vid_path = save_path
                        if isinstance(vid_writer, cv2.VideoWriter):
                            vid_writer.release()  # release previous video writer
                        if vid_cap:  # video
                            fps = vid_cap.get(cv2.CAP_PROP_FPS)
                            w = int(vid_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                            h = int(vid_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                        else:  # stream
                            fps, w, h = 30, im0.shape[1], im0.shape[0]
                            save_path += '.mp4'
                        vid_writer = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (w, h))
                    vid_writer.write(im0)

    if save_txt or save_img:
        s = f"\n{len(list(save_dir.glob('labels/*.txt')))} labels saved to {save_dir / 'labels'}" if save_txt else ''
        # print(f"Results saved to {save_dir}{s}")

    print(f'Done. ({time.time() - t0:.3f}s)')

def no_crop(img, id, path):
    cv2.imshow("cropped", img)
    cimg_name = path + "_" + str(id) + ".jpg"
    cv2.imwrite(cimg_name, img)

    ocr_model = PaddleOCR(lang='ch', use_gpu=False)  # chi_tra 在tesseract 是繁體
    img_path = os.path.join(cimg_name)
    # result = ocr_model.ocr(img_path, det=False)
    result = ocr_model.ocr(img_path)
    s = " ".join('%s' % id for id in result)  # list to string
    # output字
    x = s.split(")],")  # string split to list

    keyword = get_txtkey()
    print("keyword = ", keyword)
    all_word = np.array(x)  # list to array
    store_keyword = search_keyword(all_word, keyword)  # 在所有文本中找關鍵字的那幾列
    over_keyword = keyword_processing(store_keyword)  # 進行文字處理（去括號等

    if len(over_keyword) == 1:
        draw_pic(over_keyword[0], img)
    else:
        for i in range(len(over_keyword)):
            if i == 0:
                draw_pic(over_keyword[0], img)
            else:
                resultImg = cv2.imread("C:/Users/shin/410828608/yolov7-main/draw_result.jpg")
                draw_pic(over_keyword[i], resultImg)
    for i in x:
        print(i)


def crop_image(xy, img, id, path):
    x1 = int(xy[0])
    y1 = int(xy[1])
    x2 = int(xy[2])
    y2 = int(xy[3])
    print(x1, y1, x2, y2)
    print('id: ' + path)
    cropped_image = img[y1:y2, x1:x2]
    cv2.imshow("cropped", cropped_image)
    cimg_name = path + "_" + str(id) + ".jpg"
    cv2.imwrite(cimg_name, cropped_image)

    ocr_model = PaddleOCR(lang='ch', use_gpu=False)  # chi_tra 在tesseract 是繁體
    img_path = os.path.join(cimg_name)
    # result = ocr_model.ocr(img_path, det=False)
    result = ocr_model.ocr(img_path)
    s = " ".join('%s' % id for id in result)  # list to string
    # output字
    x = s.split(")],")  # string split to list

    keyword = get_txtkey()
    print("keyword = ", keyword)
    all_word = np.array(x)  # list to array
    store_keyword = search_keyword(all_word, keyword)  # 在所有文本中找關鍵字的那幾列
    over_keyword = keyword_processing(store_keyword)  # 進行文字處理（去括號等

    if len(over_keyword) == 1:
        draw_pic(over_keyword[0], cropped_image)
    else:
        for i in range(len(over_keyword)):
            if i == 0:
                draw_pic(over_keyword[0], cropped_image)
            else:
                resultImg = cv2.imread("C:/Users/shin/410828608/yolov7-main/draw_result.jpg")
                draw_pic(over_keyword[i], resultImg)

    for i in x:
        print(i)
    temp_img = cv2.imread("C:/Users/shin/410828608/yolov7-main/draw_result.jpg")
    cv2.imshow("result", temp_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def keyword_processing(store_keyword):
    location_list = []
    # 去掉後面的('糖', 0.9993472695350647)
    for i in range(len(store_keyword)):
        add_str = ""  # add_str用來存沒有('糖', 0.9993472695350647)的字串
        # print("i = ", i)
        if "], (" in store_keyword[i]:
            start_index = store_keyword[i].find("], (")  # 找出 "], (" 的索引值
            if start_index != -1:
                for j in range(start_index):
                    add_str = add_str + store_keyword[i][j]
            else:
                print("can not find")
        add_str = add_str.replace('[[', '')  # 去掉前面的兩個括號
        print("add_str = ", add_str)
        location_list.append(add_str)
    for i in location_list:
        print("location_list =", i)
    return location_list


def get_location(store_keyword):
    location = store_keyword.replace(' ', '')
    # [77.0, 957.0], [154.0, 957.0], [154.0, 1026.0], [77.0, 1026.0]
    float_location = []
    temp_str = ''
    sign = 0
    count = 0
    # 抓座標
    for char in location:
        if char == '[':
            count += 1
        elif char == ']':
            count += 1
        elif char == ',':
            sign += 1
            if sign == 2:
                sign = 0
                continue
        temp_str += char
        if count == 2:
            temp_list = eval(temp_str)  # string to list
            float_list = [float(coord) for coord in temp_list]  # list(item) to float
            float_location.append(float_list)
            temp_str = ''
            count = 0
    print('float_arrays =', float_location)
    return float_location


def draw_pic(store_keyword, cropped_image):
    img_np = np.asarray(cropped_image)  # 圖片轉格式，下面畫圖的function要用的
    float_location = get_location(store_keyword)

    temp_img = cv2.rectangle(img_np, (int(float_location[0][0]), int(float_location[0][1]))
                             , (int(float_location[2][0]), int(float_location[2][1]))
                             , (0, 0, 255), 3)
    # img_from_np = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)

    cv2.imwrite("C:/Users/shin/410828608/yolov7-main/draw_result.jpg", temp_img)


def search_keyword(all_words, keyword):
    arr = [0] * len(all_words)
    store_keyword = []

    for i in range(len(all_words)):
        # if operator.contains(all_words(i), keyword):
        for j in range(len(keyword)):
            if keyword[j] in all_words[i]:
                arr[i] = arr[i] + 1
    for i in range(len(arr)):
        # if arr[i] != 0:
        #     store_keyword.append(all_words[i] + ")]")
        if arr[i] == len(keyword):
            store_keyword.append(all_words[i] + ")]")
    print("contains = ", store_keyword)
    return store_keyword
    # SocketServer.send_String(store_keyword)
    # 要回傳socket包回去


def get_txtkey():
    temp = file_contents.split('"')
    key_list = []
    key = temp[1].strip('"')
    for i in key:
        key = i.strip('"')
        key_list.append(key)
    print('key_list =', key_list)
    return key_list

file_path = "C:/Users/shin/410828608/yolov7-main/store_keyword.txt"  # 指定文件的路徑
file_contents = ""
with open(file_path, "r") as file:
    file_contents = file.read()  # 讀取文件內容並存儲在file_contents變數中

print("文件內容:")
print(file_contents)

parser = argparse.ArgumentParser()
parser.add_argument('--weights', nargs='+', type=str, default='C:/Users/shin/runs/train/exp14/weights/best.pt',
                    help='model.pt path(s)')  # help()函數是查看函數或模組用途的詳細說明
parser.add_argument('--source', type=str, default='C:/Users/shin/410828608/yolov7-main/image.jpg',
                    help='source')  # file/folder, 0 for webcam
parser.add_argument('--img-size', type=int, default=640, help='inference size (pixels)')
parser.add_argument('--conf-thres', type=float, default=0.2, help='object confidence threshold')
parser.add_argument('--iou-thres', type=float, default=0.45, help='IOU threshold for NMS')
parser.add_argument('--device', default='', help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
parser.add_argument('--view-img', action='store_true', help='display results')
parser.add_argument('--save-txt', action='store_true', help='save results to *.txt')
parser.add_argument('--save-conf', action='store_true', help='save confidences in --save-txt labels')
parser.add_argument('--nosave', action='store_true', help='do not save images/videos')
parser.add_argument('--classes', nargs='+', type=int, help='filter by class: --class 0, or --class 0 2 3')
parser.add_argument('--agnostic-nms', action='store_true', help='class-agnostic NMS')
parser.add_argument('--augment', action='store_true', help='augmented inference')
parser.add_argument('--update', action='store_true', help='update all models')
parser.add_argument('--project', default='runs/detect', help='save results to project/name')
parser.add_argument('--name', default='exp', help='save results to project/name')
parser.add_argument('--exist-ok', action='store_true', help='existing project/name ok, do not increment')
parser.add_argument('--no-trace', action='store_true', help='don`t trace model')
opt = parser.parse_args()

# opencv裁剪yolo擷取到的範圍
# 存到某個變數 + 放在path裡面
# assign給img_path後, 再從img_path裡辨識文字
print(opt)

with torch.no_grad():
    if opt.update:  # update all models (to fix SourceChangeWarning)
        for opt.weights in ['C:/Users/shin/runs/train/exp14/weights/best.pt']:
            detect()
            strip_optimizer(opt.weights)
    else:
        detect()