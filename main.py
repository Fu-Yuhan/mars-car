import time

from Function import LookForObj, TaskRock
from Function.LineFollower import LineFollowMgr
import Camera
import math
import threading
import cv2
import numpy as np
from blue import sim_turn
true=True
def find_sign():
    global status
    global camera
    global turn_side
    camera_get=threading.Thread(target=camera.camera_task())
    camera_get.setDaemon(True)
    camera_get.start()
    turn_time=0
    while True:
        img = camera.frame
        if img is not None:
            sim=sim_turn(img)
            if sim:
                if sim=='left' and turn_time>=0:
                    turn_time=turn_time+1
                elif sim=='left' and turn_time<0:
                    turn_time=turn_time+2
                elif sim=='right' and turn_time<=0:
                    turn_time=turn_time-1
                elif sim=='right' and turn_time>0:
                    turn_time=turn_time-2
                if turn_time>=3:
                    turn_side='left'
                    exit()
                elif turn_time<=-3:
                    turn_side='right'
                    exit()
            else:
                time.sleep(0.2)
            #left = cv2.imread('left.jpg', 0)
            #right = cv2.imread('right.jpg', 0)
            #cv2.imshow('img', img)



def main():

    # 任务1 巡线
    turn_time = 3# 转弯时间
    status = "not started"
    # 初始化底盘
    car = LineFollowMgr()
    turn_side = None
    car.reset()
    car.start()
    status = "before detected"
    # 初始化摄像头
    camera = Camera.Camera()
    camera.camera_open(correction=True)

    while True:
        #find_sign()
        find_signs=threading.Thread(target=find_sign())
        find_signs.start()
        if not turn_side == None:
            print(turn_side)
        # TODO:检测路标
        # TODO: status = "after detected"
        # 检测前方路况
        sonar = car.line.readData()
        if sonar[0] & sonar[1] & sonar[2] & sonar[3]:# 遇到转弯1
            car.stop()
            car.car.set_velocity(math.pi*(car.car.a**2)/(4*turn_time),90,math.pi/(2*turn_time))# TODO:根据识别的结果左转或右转
            time.sleep(turn_time)
            car.start()
            status = "after first cross"

        # TODO: status = "after carried rocks"
        # TODO: status = "after lunched rocket"

        if sonar[0] and sonar[1] and sonar[2] and not sonar[3]:
            car.stop()
            car.car.set_velocity(math.pi * (car.car.a ** 2) / (4 * turn_time), 90,
                                 math.pi / (2 * turn_time))  # 左转
            time.sleep(turn_time)
            car.start()
            status = "after 2nd cross"

        if not sonar[0] and sonar[1] and sonar[2] and sonar[3]:
            car.stop()
            car.car.set_velocity(math.pi * (car.car.a ** 2) / (4 * turn_time), 90,
                                 -math.pi / (2 * turn_time))  # 左转
            time.sleep(turn_time)
            car.start()
            status = "after 2nd cross"










if __name__ == "__main__":
    main()
