import cv2
import numpy as np
from PIL import Image

from skimage.metrics import structural_similarity
time=0
def similar_test(image1, image2):
    global time
    time+=1
    image1_ = cv2.resize(image1, (10,10))
    image2_ = cv2.resize(image2, (10,10))
    score=0
    for y in range(10):
        for x in range(10):
            xiang1 = image1_[y, x]
            xiang2 = image2_[y, x]
            if xiang1== xiang2 :
                score+=1
    print(score)
    return score
def similar(image1, image2):
    global time
    time+=1
    image1_ = cv2.resize(image1, (32,32))
    #cv2.imshow('image1'+str(time), image1_)
    image2_ = cv2.resize(image2, (32,32))
    #cv2.imshow('image2'+str(time), image2_)
    # 灰度直方图算法
    # 计算单通道的直方图的相似值
    '''
    cv2.imshow('image1',image1_)
    cv2.imshow('image2',image2_)
    cv2.waitKey(0)
    '''
    hist1 = cv2.calcHist([image1_], [0], None, [256], [0.0, 255.0])
    hist2 = cv2.calcHist([image2_], [0], None, [256], [0.0, 255.0])
    # 计算直方图的重合度
    degree = 0
    for i in range(len(hist1)):
        if hist1[i] != hist2[i]:
            degree = degree + \
                (1 - abs(hist1[i] - hist2[i]) / max(hist1[i], hist2[i]))
        else:
            degree = degree + 1
    degree = degree / len(hist1)
    return degree
    '''
def similar(image1, image2, size=(256, 256)):
    # RGB每个通道的直方图相似度
    # 将图像resize后，分离为RGB三个通道，再计算每个通道的相似值
    image1 = cv2.resize(image1, size)
    image2 = cv2.resize(image2, size)
    sub_image1 = cv2.split(image1)
    sub_image2 = cv2.split(image2)
    sub_data = 0
    for im1, im2 in zip(sub_image1, sub_image2):
        sub_data += calculate(im1, im2)
    sub_data = sub_data / 3
    return sub_data
    '''
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
    '''
def find_blue_edge(img):
    mask = find_blue(img)
    # 边缘检测
    edges = cv2.Canny(mask, threshold1=50, threshold2=150)
    #edges=cv2.approxPolyDP()
    #contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return edges
    '''
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
def largest_large(binary_image):
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        return None

    largest_contour = max(contours, key=cv2.contourArea)

    # 普通外接矩形
    x, y, w, h = cv2.boundingRect(largest_contour)
    bounding_rect_image = binary_image[y:y+h, x:x+w]

    return bounding_rect_image
#cv2.destroyAllWindows()
def similation(img1,img2):
    ppp=[]
    '''
    cv2.imshow('img1',img1)
    cv2.imshow('img2',img2)
    cv2.waitKey(0)
    '''
    for i in range(4):
        img2_=img2
        img2_=np.rot90(img2_, i)
        sim=similar_test(img1,img2_)
        #print(sim)
        ppp.append(sim)
        #cv2.imshow('img1'+str(i+1),img1)
        #cv2.imshow('img2'+str(i+1),img2_)
    return max(ppp)
def main(img,img2):
    #print(img2.shape)
    size=min(img2.shape[1],img2.shape[0])
    #print(size)
    #img2=cv2.GaussianBlur(img2, (5, 5), 0)
    #mask = find_red(img)6400*3200
    #mask = find_red(img)
    # 边缘检测
    #edges = cv2.Canny(mask, threshold1=50, threshold2=150)
    #hist = cv2.calcHist([mask], [0], None, [256], [0, 256])
    edges  = find_blue(img)
    edges2 = find_blue(img2)
    large = largest(edges2)
    if  large is None:
        return None
    large_=cv2.bitwise_not(large)
    large_size=large.shape
    a,b,c,d=int(large_size[0]/9),int(large_size[0]*8/9),int(large_size[1]/9),int(large_size[1]*8/9)
    large_=large_[a:b,c:d]
    large=largest_large(large_)
    '''
    cv2.imshow('img', large)
    cv2.imshow("edges",edges)
    cv2.imshow("edges2",edges2)
    cv2.waitKey(0)
    '''
    if  large is None:
        return None
    cv2.waitKey(0)
    #print(large.shape)
    if large.shape[0]<size*0.06 or large.shape[1]<size*0.06:
        return None
    #edges_lest=  largest(edges)
    edges=cv2.bitwise_not(edges)
    edges=largest_large(edges)

    edges_lest=edges
    sim=similation(edges_lest,large)
    #direction = recognize_direction(edges)
    '''
    cv2.imshow("edges",edges)
    cv2.imshow("edges_left",edges_lest)
    #cv2.imshow("hist",hist)
    cv2.imshow("edges2",edges2)
    #print(edges2)
    cv2.imshow("large",large)
    cv2.imshow("main",largest(edges2))
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    '''
    return sim
def sim_turn(img2,img_left=None,img_right=None):
    if img_left is None:
        img_left = cv2.imread('left.jpg')
    if img_right is None:
        img_right= cv2.imread('right.jpg')
    #img2= cv2.imread('test.jpg')
    sim_left=main(img_left,img2)
    sim_right=main(img_right,img2)
    if sim_left and sim_right:
        if sim_right>sim_left:
            return 'right'
        elif sim_right<sim_left:
            return 'left'
        else:
            return None
    else:
        return None
if  __name__ == '__main__':
    import os
    paths = os.walk(r'./test/test')
    for path, dir_lst, file_lst in paths:
        for file_name in file_lst:
            print(file_name)
            img=cv2.imread('test\\test\\'+file_name)
            print(sim_turn(img))
#img=cv2.imread('.jpg')
#print(sim_turn(img))