import base64
import BaiduObjDetect
import time
from HiwonderSDK.mecanum import MecanumChassis
import cv2

from HiwonderSDK.Board import setPWMServoPulse
def grab_and_move():
    print('starting: grab and move')
    cap = cv2.VideoCapture(-1)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    print('camera opened')
    car = MecanumChassis()
    # 调整姿态至正对位置
    while True:

        ret, frame = cap.read()
        success, encoded_images = cv2.imencode('.jpg',frame, [int(cv2.IMWRITE_JPEG_QUALITY), 85])
        if success:
            frame_base64 = base64.b64encode(encoded_images).decode('utf-8')
            results = BaiduObjDetect.find_obj(frame_base64)
            biggest = {'location': {'height': 0, 'left': 0, 'top': 0, 'width': 0}, 'name': None, 'score': 0}
            for result in results['result']:
                if result['location']['height'] * result['location']['width'] >= biggest['location']['height'] * biggest['location']['width']:
                    biggest = result

            middle = biggest['location']['left'] + biggest['location']['width']
            if middle >= 340:

                car.translation(-5, 0)
            if middle <= 300:
                car.translation(5, 0)
            else:
                break# 退出循环
        else:
            print('camera error')
        time.sleep(0.1)
    setPWMServoPulse(1, 1500, 500)
    # TODO:机械臂到位
    print("已经居中")
    while True:
        car.set_velocity(35, 90, 0)
        ret, frame = cap.read()
        success, encoded_images = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 85])
        if success:
            frame_base64 = base64.b64encode(encoded_images).decode('utf-8')
            results = BaiduObjDetect.find_obj(frame_base64)
            biggest = {'location': {'height': 0, 'left': 0, 'top': 0, 'width': 0}, 'name': None, 'score': 0}
            for result in results['result']:
                if result['location']['height'] * result['location']['width'] >= biggest['location']['height'] * \
                        biggest['location']['width']:
                    biggest = result
            middle = biggest['location']['top']-biggest['location']['height']/2
            if middle <= 480 - 80:# TODO:能抓到的地方
                setPWMServoPulse(1, 1900, 500)
                break
    position = 10# TODO:量好预定距离
    car.translation(0,position)
    # TODO:放置
    setPWMServoPulse(1, 1500, 500)
    car.translation(0,-position)

if __name__ == '__main__':

    grab_and_move()