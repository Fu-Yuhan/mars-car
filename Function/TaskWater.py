import base64
import time

import cv2

import Camera
from Function.BaiduObjDetect import find_obj
from HiwonderSDK.mecanum import MecanumChassis


def grab_and_move(position):
    camara = Camera.Camera()
    camara.camera_open(correction=True)
    car = MecanumChassis()
    while True:
        cap = camara.cap
        ret, frame = cap.read()
        success, encoded_images = cv2.imencode('.jpg',frame, [int(cv2.IMWRITE_JPEG_QUALITY), 85])
        if success:
            frame_base64 = base64.b64encode(encoded_images).decode('utf-8')
            results = find_obj(frame_base64)
            biggest = {'location': {'height': 0, 'left': 0, 'top': 0, 'width': 0}, 'name': None, 'score': 0}
            for result in results['result']:
                if result['location']['height'] * result['location']['width'] >= biggest['location']['height'] * biggest['location']['width']:
                    biggest = result
            middle = biggest['location']['left']+biggest['location']['width']/2
            if middle >= 340:
                car.translation(5, 0)
            if middle <= 300:
                car.translation(-5, 0)
            else:
                break  # 退出循环
        time.sleep(0.1)
    while True:
        car.set_velocity(35, 90, 0)
        cap = camara.cap
        ret, frame = cap.read()
        success, encoded_images = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 85])
        if success:
            frame_base64 = base64.b64encode(encoded_images).decode('utf-8')
            results = find_obj(frame_base64)
            biggest = {'location': {'height': 0, 'left': 0, 'top': 0, 'width': 0}, 'name': None, 'score': 0}
            for result in results['result']:
                if result['location']['height'] * result['location']['width'] >= biggest['location']['height'] * biggest['location']['width']:
                    biggest = result
            middle = biggest['location']['top']-biggest['location']['height']/2
                # TODO:判断什么时候能抓取
            if True:
                car.translation(0, 0)
                break
    #TODO:合抓
    car.translation(-100 if position == "left" else 100,50)
