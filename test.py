import cv2
import numpy as np
from encode import encode
from numba import jit
from random import randint
import copy
from appraise_PSNR import appraise_PSNR

RGB = np.array([0.299, 0.587, 0.114])


def predictV(value, grayij, X):
    beta = np.linalg.pinv(X.T * X) * X.T * value
    r_predict = np.linalg.det([1, grayij, grayij**2] * beta)
    if r_predict <= min(value[1, 0], value[0, 0]): r_predict = min(value[1, 0], value[0, 0])
    elif r_predict >= max(value[1, 0], value[0, 0]):
        r_predict = max(value[1, 0], value[0, 0])
    return np.round(r_predict)


def PEs(gray, img):
    pError = np.zeros(img.shape)
    predict = img.copy()
    rho = np.zeros(gray.shape)
    for i in range(1, img.shape[0] - 1):
        for j in range(1, img.shape[1] - 1):
            r = np.array([img[i + 1, j, 0], img[i, j + 1, 0], img[i + 1, j + 1, 0]]).reshape(3, 1)
            b = np.array([img[i + 1, j, 2], img[i, j + 1, 2], img[i + 1, j + 1, 2]]).reshape(3, 1)
            gr = np.array([gray[i + 1, j], gray[i, j + 1], gray[i + 1, j + 1]]).reshape(3, 1)
            X = np.mat(np.column_stack(([1] * 3, gr, gr**2)))
            predict[i, j, 0] = predictV(r, gray[i, j], X)
            predict[i, j, 2] = predictV(b, gray[i, j], X)
            pError[i, j] = img[i, j] - predict[i, j]
            rho[i, j] = np.var([gray[i - 1, j], gray[i, j - 1], gray[i, j], gray[i + 1, j], gray[i, j + 1]], ddof=1)
    return predict, pError, rho


def invariant(rgb):
    return np.round(rgb[:2].dot(RGB[:2]) + 2 * (rgb[2] // 2) * RGB[2]) == np.round(rgb[:2].dot(RGB[:2]) +
                                                                                   (2 * (rgb[2] // 2) + 1) * RGB[2])


def embedMsg(img, gray, mesL, selected, predict, pError, Dt):
    IMG, GRAY, pERROR = img.copy(), gray.copy(), pError.copy()
    tags = []
    La = 0
    tagsCode = '0'
    ec = 0
    location = 0
    msg = [int(i) for i in str(bin(2**19999))[2:]]
    # msg = [1, 0, 0]
    msgIndex = 0
    for i in zip(*selected):
        if tags.count(0) < mesL:
            # 遍历满足rho<rhoT的像素点进行插入信息
            pERROR[i][0] = 2 * pERROR[i][0] + msg[msgIndex]
            pERROR[i][2] = 2 * pERROR[i][2] + ec
            rgb = np.array([predict[i][loc] + pERROR[i][loc] for loc in range(3)])
            rgb[1] = np.round((GRAY[i] - rgb[0] * RGB[0] - rgb[2] * RGB[2]) / RGB[1])
            ec = abs(IMG[i][1] - rgb[1])
            D = np.linalg.norm(rgb - IMG[i])
            if np.max(rgb) > 255 or np.min(rgb) < 0 or D > Dt:
                tags.append(1)  # 设置当前的tag为非法（tag为1）
            else:
                # print(f'{i}, {img[i]}, {rgb}')
                tags.append(0)
                msgIndex += 1
                IMG[i] = rgb
        else:
            if La == 0:
                if np.unique(tags).size > 1:
                    tagsCode, La = encode(tags)
                else:
                    La = 1
            if location == La: break
            if invariant(IMG[i]):
                IMG[i][2] = 2 * (IMG[i][2] // 2) + int(tagsCode[location])
                location += 1
    if len(tags) < mesL or location < La: return False, ec, La, len(tags), tagsCode, msg
    print(f"msg: {int(''.join([str(i) for i in msg]), 2)}")
    return (IMG, GRAY, pERROR), ec, La, len(tags), tagsCode, msg


if __name__ == '__main__':
    import sys
    Size = None
    msg = ''
    if 1:
        img = cv2.imread('./lena.png')
        psnr_img = copy.copy(img)
        print("psnr" + str(appraise_PSNR(psnr_img, img)))
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY).astype(np.int32)[:Size, :Size]
        img = img.astype(np.int32)[:Size, :Size]
        # cv2.imshow('src', img)
        # cv2.waitKey()
        predict, pError, rho = PEs(gray, img)
        #
        Dt = 20
        mesL = int(20000)
        flag = 1
        rhoT = 0
        #
        while np.count_nonzero(rho < rhoT) <= mesL:
            rhoT += 1
        #
        enough = 0
        while not enough:
            selected = [n + 1 for n in np.where(rho[1:-1, 1:-1] < rhoT)]
            print(selected[0].size)
            if selected[0].size >= (img.shape[0] - 2)**2:
                print('The picture is too small')
                exit()
            enough, lastEc, La, N, tagsCode, msg = embedMsg(img, gray, mesL, selected, predict, pError, Dt)
            rhoT += 0 if enough else 1
        img, gray, pError = enough

        # print("psnr-- " + str(appraise_PSNR(psnr_img, img)))
        #
        border = sorted(
            list(
                set(map(tuple, np.argwhere(gray == gray))) -
                set(map(tuple,
                        np.argwhere(gray[1:-1, 1:-1] == gray[1:-1, 1:-1]) + 1))))
        border = list(filter(lambda xy: invariant(img[xy]), border))
        if len(border) < 40: print('The size of image is too small to contain the necessary parameters')
        for char, loc in zip(f'{rhoT:016b}' + f'{int(lastEc):08b}' + f'{La:016b}' + f'{N:016b}',
                             filter(lambda xy: invariant(img[xy]), border)):
            img[loc][2] = 2 * (img[loc][2] // 2) + int(char)
        cv2.imwrite('./Slena.png', img)
        print(rhoT, int(lastEc), La, N, tagsCode)
        print("psnr: " + str(appraise_PSNR(psnr_img, img)))

        imgRcv = cv2.imread('./Slena.png')
        grayRcv = cv2.cvtColor(imgRcv, cv2.COLOR_RGB2GRAY).astype(np.int32)[:Size, :Size]
        imgRcv = imgRcv.astype(np.int32)[:Size, :Size]
        predictRcv, pErrorRcv, rhoRcv = PEs(grayRcv, imgRcv)
        border = sorted(
            list(
                set(map(tuple, np.argwhere(grayRcv == grayRcv))) -
                set(map(tuple,
                        np.argwhere(grayRcv[1:-1, 1:-1] == grayRcv[1:-1, 1:-1]) + 1))))
        border = [str(imgRcv[loc][2] % 2) for loc in filter(lambda xy: invariant(imgRcv[xy]), border)]
        rhoT = int(''.join(border[:16]), 2)
        lastEc = int(''.join(border[16:24]), 2)
        La = int(''.join(border[24:40]), 2)
        N = int(''.join(border[40:56]), 2)
        selected = [tuple(n + 1) for n in np.argwhere(rhoRcv[1:-1, 1:-1] < rhoT)]
        tagsCode = [imgRcv[value][2] % 2
                    for value in filter(lambda xy: invariant(imgRcv[xy]), selected[N:])][:La] if La != 1 else [0] * N
        print(rhoT, lastEc, La, N, ''.join([str(i) for i in tagsCode]))

        candidate = reversed([selected[:N][index] for index, value in enumerate(tagsCode) if value == 0])
        predictRcv = imgRcv.copy()
        pErrorRcv = np.zeros(imgRcv.shape)
        msgRcv = []
        for i in candidate:
            rM = np.array([imgRcv[i[0] + 1, i[1], 0], imgRcv[i[0], i[1] + 1, 0],
                           imgRcv[i[0] + 1, i[1] + 1, 0]]).reshape(3, 1)
            bM = np.array([imgRcv[i[0] + 1, i[1], 2], imgRcv[i[0], i[1] + 1, 2],
                           imgRcv[i[0] + 1, i[1] + 1, 2]]).reshape(3, 1)
            grM = np.array([grayRcv[i[0] + 1, i[1]], grayRcv[i[0], i[1] + 1],
                            grayRcv[i[0] + 1, i[1] + 1]]).reshape(3, 1)
            X = np.mat(np.column_stack(([1] * 3, grM, grM**2)))
            predictRcv[i][0] = predictV(rM, grayRcv[i], X)
            predictRcv[i][2] = predictV(bM, grayRcv[i], X)
            pErrorRcv[i] = imgRcv[i] - predictRcv[i]
            msgRcv.append(int(pErrorRcv[i][0]) % 2)
            nextEc = pErrorRcv[i][2] % 2
            pErrorRcv[i] = pErrorRcv[i] // 2
            gRcv = imgRcv[i][1]
            imgRcv[i] = predictRcv[i] + pErrorRcv[i]
            # imgRcv[i][1] = np.round((grayRcv[i] - imgRcv[i][0] * RGB[0] - imgRcv[i][2] * RGB[2]) / RGB[1])
            if np.round(np.array([imgRcv[i][0], imgRcv[i][1] + lastEc, imgRcv[i][2]]).dot(RGB)) == grayRcv[i]:
                imgRcv[i][1] += lastEc
            elif np.round(np.array([imgRcv[i][0], imgRcv[i][1] - lastEc, imgRcv[i][2]]).dot(RGB)) == grayRcv[i]:
                imgRcv[i][1] -= lastEc
            elif np.round(np.array([imgRcv[i][0], imgRcv[i][1] - lastEc, imgRcv[i][2]]).dot(RGB)) != grayRcv[i]:
                # print(f"index {i} has no matched ec")
                pass

            lastEc = abs(nextEc)
        print(f"msg: {int(''.join([str(i) for i in list(reversed(msgRcv))]), 2)}")
        print(''.join([str(i) for i in msg]) == ''.join([str(i) for i in list(reversed(msgRcv))]))
