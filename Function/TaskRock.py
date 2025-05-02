import base64
import BaiduObjDetect

from statsmodels.stats.libqsturng.make_tbls import success
import cv2
import Camera
def move2front():
    camara = Camera.Camera()
    camara.camera_open(correction=True)
    # 调整姿态至正对位置
    while True:
        cap = camara.cap
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
                pass# TODO:向右移动
            if middle <= 300:
                pass# TODO:向左移动
            else:
                break# 退出循环
    # TODO:机械臂到位

    while True:
        # TODO:前进
        cap = camara.cap
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
        if middle <= 160:# 能抓到的地方
            # TODO:合抓
            break
    # TODO:前进预定的距离
    # TODO:放置
    # TODO:后退

