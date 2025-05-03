import time

from Function import LookForObj, TaskRock
from Function.LineFollower import LineFollowMgr
import Camera
import math
true=True
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
        # TODO:检测路标
        # TODO: status = "after detected"
        # 检测前方路况
        sonar = car.line.readData()
        if sonar[0] & sonar[1] & sonar[2] & sonar[3]:# 遇到转弯1
            car.stop()
            car.car.set_velocity(math.pi*(car.car.a**2)/(4*turn_time),90,math.pi/(2*turn_time))# TODO:根据识别的结果左转或右转
            time.sleep(turn_time)# TODO:增加末尾运水的判定
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

        try:
            if LookForObj.look_for_obj():
                car.stop()
                # TODO: 根据识别结果检测要用哪个
                TaskRock.grab_and_move()
                car.start()
        except Exception as e:
            print(e)











if __name__ == "__main__":
    main()
