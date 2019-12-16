import math
import numpy as np
from addPEs import addPEs
from appraise_PSNR import appraise_PSNR


def main(messL, D_T, gray, cover, PER, PEB, pred_R, pred_B, cost):
    # 找到局部方差小于ρT的足够多的三元组（数目大于messL）
    # 代码涉及部分:Algorithm 1 Pseudo Code of Selecting Lr,ρT and DT
    for T in range(0, 10**10, 1):
        if len(np.where(cost <= T)) > messL:
            break

        if len(np.where(cost <= T)) >= len(cost):
            raise ValueError("Too large payloads")

    # 执行addPEs加密图像，得到L_a比特的辅助信息
    tag = 0
    while not tag:
        sel_ind = np.where(cost <= T)
        lsb_ind = np.where(cost >= T)
        stego, L_embedmess, L_a, tag, N = addPEs(gray, cover, PER, PEB, pred_R, pred_B, sel_ind, lsb_ind, messL, D_T**2)
        T = T + 1
    T = T - 1
    messL = L_embedmess - L_a
    '''
    代码涉及部分:
    IV.  EXPERIMENTAL RESULTS
    A. Payload-Distortion Performance
    '''
    # 计算PSNR进行评估
    psnr = appraise_PSNR(cover, stego)
    R_Gray = np.round(0.299 * stego[:, :, 2] + 0.587 * stego[:, :, 1] + 0.114 * stego[:, :, 0])
    as_ = (R_Gray[:]).astype('float64') - (gray[:]).astype('float64')
    graydiff = sum(abs(as_))
    return messL, psnr, T, N
