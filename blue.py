import cv2
import numpy as np
from PIL import Image
 
def find_blue(img):
    #img = cv2.imread('left.jpg')
    # 在彩色图像的情况下，解码图像将以b g r顺序存储通道。
    grid_RGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
 
    # 从RGB色彩空间转换到HSV色彩空间
    grid_HSV = cv2.cvtColor(grid_RGB, cv2.COLOR_RGB2HSV)
 
    # H、S、V范围一：
    #lower1 = np.array([100,43,46])
    lower1 = np.array([100,80,80])
    upper1 = np.array([124,255,255])
    mask = cv2.inRange(grid_HSV, lower1, upper1)       # mask1 为二值图像
    #res1 = cv2.bitwise_and(grid_RGB, grid_RGB, mask=mask1)
 
    # H、S、V范围二：
    '''
    lower2 = np.array([156,43,46])
    upper2 = np.array([180,255,255])
    mask2 = cv2.inRange(grid_HSV, lower2, upper2)
    res2 = cv2.bitwise_and(grid_RGB,grid_RGB, mask=mask2)
    '''
 
    # 将两个二值图像结果 相加
    #mask3 = mask1 + mask2
    return  mask
    # 结果显示
    '''
    cv2.imshow("mask3", mask3)
    cv2.imshow("img",img)
    cv2.imshow("Mask1",mask1)
    cv2.imshow("res1",res1)
    cv2.imshow("Mask2",mask2)
    cv2.imshow("res2",res2)
    cv2.imshow("grid_RGB", grid_RGB[:,:,::-1])           # imshow()函数传入的变量也要为b g r通道顺序
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    '''
def find_blue_edge(img):
    mask = find_blue(img)
    # 边缘检测
    edges = cv2.Canny(mask, threshold1=50, threshold2=150)
    #edges=cv2.approxPolyDP()
    #contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return edges

def largest(binary_image):
    """
    在二值图像中查找面积最大的轮廓，并返回其最小外接旋转矩形范围内的图像。

    参数:
        binary_image (np.ndarray): 输入的二值图像（单通道）。

    返回:
        np.ndarray: 面积最大的轮廓对应的最小旋转矩形区域内的图像。
    """
    # 查找所有轮廓
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        return None  # 如果没有找到轮廓，返回None

    # 找到面积最大的轮廓
    largest_contour = max(contours, key=cv2.contourArea)

    # 获取包围该轮廓的最小旋转矩形
    rect = cv2.minAreaRect(largest_contour)
    box = cv2.boxPoints(rect)  # 获取矩形的四个顶点坐标
    box = np.int0(box)         # 转换为整数坐标

    # 获取矩形的宽高
    width = int(rect[1][0])
    height = int(rect[1][1])

    # 构造目标矩形的四个角点（用于透视变换）
    dst_pts = np.array([[0, height],
                        [0, 0],
                        [width, 0],
                        [width, height]], dtype="float32")

    # 计算透视变换矩阵
    M = cv2.getPerspectiveTransform(np.float32(box), dst_pts)

    # 应用透视变换，获取矫正后的图像区域
    warped = cv2.warpPerspective(binary_image, M, (width, height))

    return warped
#cv2.destroyAllWindows()
if __name__ == "__main__":
    img = cv2.imread('left.jpg')
    img2= cv2.imread('test.jpg')
    #img2=cv2.GaussianBlur(img2, (5, 5), 0)
    #mask = find_red(img)
    # 边缘检测
    #edges = cv2.Canny(mask, threshold1=50, threshold2=150)
    #hist = cv2.calcHist([mask], [0], None, [256], [0, 256])
    edges  = find_blue(img)
    edges2 = find_blue(img2)
    #direction = recognize_direction(edges)
    cv2.imshow("edges",edges)
    #cv2.imshow("hist",hist)
    cv2.imshow("edges2",edges2)
    #print(edges2)
    cv2.imshow("main",largest(edges2))
    cv2.waitKey(0)
    cv2.destroyAllWindows()