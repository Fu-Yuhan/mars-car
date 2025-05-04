from BaiduObjDetect import find_obj
import cv2

import base64
KEY_WORDS = [

]
def look_for_obj():

    cap = cv2.VideoCapture(-1)
    ret, frame = cap.read()
    success, encoded_images = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 85])
    if success:
        frame_base64 = base64.b64encode(encoded_images).decode('utf-8')
        results = find_obj(frame_base64)

        for result in results['result']:
            if result['name'] in KEY_WORDS:
                return result['name']

        return None
    raise ValueError('Camera error')