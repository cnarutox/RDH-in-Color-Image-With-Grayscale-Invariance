import cv2
import cost
from LSpredictor import LSpredictor as lsp
import numpy as np


def getPEs(gray, imgs):
    '''该函数对应论文第二部分B：基于灰度版本的多项式预测'''
    # 根据图像的不同通道得到图像的R、B的矩阵
    R = imgs[:, :, 2].astype('float64')
    B = imgs[:, :, 0].astype('float64')
    # 获取图像的高和宽
    height, width = gray.shape[0], gray.shape[1]
    array_size = (height - 2) * (width - 2)
    # 初始化所有矩阵并全部赋值为0
    # tmp_dif_R为R通道的Prediction Errors (PE预测错误率)
    tmp_dif_R = np.zeros(array_size)
    # tmp_dif_B为B通道的Prediction Errors (PE预测错误率)
    tmp_dif_B = np.zeros(array_size)
    # tmp_pred_R为R通道的预测值, 计算方法见论文公式(11)
    tmp_pred_R = np.zeros(array_size)
    # tmp_pred_B为B通道的预测值, 计算方法见论文公式(11)
    tmp_pred_B = np.zeros(array_size)
    # tmp_cost_RB为样本方差的无偏估计
    tmp_cost_RB = np.zeros(array_size)
    # tmp_gray为图像像素点的灰度值
    tmp_gray = np.zeros(array_size)

    id = 0
    for i in range(1, height - 1):
        for j in range(1, width - 1):
            # XR, XB, XGray保存当前像素右侧、下方和右下方邻近的三个位置的像素的R通道、B通道和灰度值
            # 算法思想启发来自于MED算法，但是效果优于MED算法，相关图表见论文中Figure(2)和Figure(4)
            XR = [R[i + 1][j], R[i][j + 1], R[i + 1][j + 1]]
            XB = [B[i + 1][j], B[i][j + 1], B[i + 1][j + 1]]
            XGray = [gray[i + 1][j], gray[i][j + 1], gray[i + 1][j + 1]]
            # 调用LSPredicator求R和B通道的预测值, 计算方法见论文公式(8)、(9)、(10)
            tmp_pred_R[id] = lsp(XGray, XR, gray[i][j])
            tmp_pred_B[id] = lsp(XGray, XB, gray[i][j])
            # 计算预测的误差PE，计算方法见论文公式(12)
            tmp_dif_R[id] = R[i][j] - tmp_pred_R[id]
            tmp_dif_B[id] = B[i][j] - tmp_pred_B[id]
            # 求样本方差的无偏估计rho(设置ddof=1), 计算方法见论文公式(17)
            tmp_cost_RB[id] = cost(
                [gray[i - 1][j], gray[i][j - 1], gray[i][j], gray[i + 1][j], gray[i][j + 1]])
            tmp_gray[id] = gray[i][j]
            id += 1
    # 返回R、B通道的PE矩阵和预测矩阵，以及图像的灰度值和方差的无偏估计矩阵用于后续部分的计算
    return tmp_dif_R[:id], tmp_dif_B[:id], tmp_gray[:id], tmp_pred_R[:id], tmp_pred_B[:id], tmp_cost_RB[:id]


# filename = 'lena.png'
# cover = cv2.imread(filename).astype('float64')
# cR = 0.299
# cG = 0.587
# cB = 0.114
# gray_img = np.round(cR*cover[:, :, 2]+cG*cover[:, :, 1]+cB*cover[:, :, 0])
# a, b, c, d, e, f = getPEs(gray_img, cover)
# print(f[225211])
