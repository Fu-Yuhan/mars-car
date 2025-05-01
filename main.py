import time

from Function.LineFollower import LineFollowMgr
import Camera
import math
true=True
def main():
    # 任务1 巡线
    turn_time = 3
    # 初始化底盘
    car = LineFollowMgr()
    car.reset()
    car.start()
    # 初始化摄像头
    camera = Camera.Camera()
    camera.camera_open(correction=True)

    while True:
        # TODO:检测路标

        # 检测前方路况
        sonar = car.line.readData()
        if sonar[0] & sonar[1] & sonar[2] & sonar[3]:# 遇到转弯1
            car.stop()
            car.car.set_velocity(math.pi*(car.car.a**2)/(4*turn_time),90,math.pi/(2*turn_time))# TODO:根据识别的结果左转或右转
            time.sleep(turn_time)
            car.start()









if __name__ == "__main__":
    main()
