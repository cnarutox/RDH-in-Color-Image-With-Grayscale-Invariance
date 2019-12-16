from random import randint

import cv2
import matplotlib.pyplot as plt
import numpy as np
from numba import jit

from encode import encode

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
    predict = img.copy().astype(np.int32)
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


def embedMsg(img, gray, msg, mesL, selected, predict, pError, Dt):
    IMG, GRAY, pERROR = img.copy(), gray.copy(), pError.copy()
    tags = []
    La = 0
    tagsCode = '0'
    ec = 0
    location = 0
    msg = [int(i) for i in msg]
    msgIndex = 0
    for i in zip(*selected):
        if tags.count(0) < mesL:
            # 遍历满足rho<rhoT的像素点进行插入信息
            pERROR[i][0] = 2 * pERROR[i][0] + msg[msgIndex]
            pERROR[i][2] = 2 * pERROR[i][2] + ec
            ec = abs(int(IMG[i][1] - np.round((GRAY[i] - IMG[i][0] * RGB[0] - IMG[i][2] * RGB[2]) / RGB[1])))
            rgb = np.array([predict[i][loc] + pERROR[i][loc] for loc in range(3)])
            rgb[1] = np.floor((GRAY[i] - rgb[0] * RGB[0] - rgb[2] * RGB[2]) / RGB[1])
            if np.round(rgb.dot(RGB)) != GRAY[i]:
                rgb[1] = np.ceil((GRAY[i] - rgb[0] * RGB[0] - rgb[2] * RGB[2]) / RGB[1])
            # rgb[1] = np.round((GRAY[i] - rgb[0] * RGB[0] - rgb[2] * RGB[2]) / RGB[1])
            if np.round(rgb.dot(RGB)) != GRAY[i]: print('!!!!!!!!!!!!!')
            D = np.linalg.norm(rgb - IMG[i])
            if np.max(rgb) > 255 or np.min(rgb) < 0 or D > Dt:
                tags.append(1)  # 设置当前的tag为非法（tag为1）
            else:
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
    if len(tags) < mesL or location < La: return False, ec, La, len(tags), tagsCode
    print(f"=> Message: {int(''.join([str(i) for i in msg]), 2)}")
    return (IMG, GRAY, pERROR), ec, La, len(tags), tagsCode


def cvtGray(img):
    gray = np.zeros(img.shape[:-1])
    for i in np.argwhere(img[:, :, -1]):
        gray[i] = np.round(img[i].dot(RGB))
    return gray


if __name__ == '__main__':
    Size = 40
    msg = 314159265659314159265659314159265659314159265659
    img = cv2.imread('./lena.png')[:Size, :Size]
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    gray = cvtGray(img)

    plt.figure(figsize=(12, 6)), plt.suptitle('Grayscale')
    plt.subplot(1, 2, 1), plt.title('Origin')
    plt.hist(gray.ravel(), 256)
    plt.show(block=False)
    print(f'{img}\n=> Finish reading image!')
    predict, pError, rho = PEs(gray, img)
    print(f'=> Finish calculating predication error!')
    #
    Dt = 20
    mesL = len(bin(msg)) - 2
    rhoT = 0
    #
    while np.count_nonzero(rho < rhoT) <= mesL:
        if np.count_nonzero(rho < rhoT) == rho.size:
            print('=> The picture is too small! Exit!')
            exit()
        rhoT += 1
    #
    enough = 0
    while not enough:
        selected = [n + 1 for n in np.where(rho[1:-1, 1:-1] < rhoT)]
        if selected[0].size >= (img.shape[0] - 2)**2:
            print('=> The picture is too small! Exit!')
            exit()
        enough, lastEc, La, N, tagsCode = embedMsg(img, gray, str(bin(msg)[2:]), mesL, selected, predict, pError, Dt)
        rhoT += 0 if enough else 1
    print(f'=> Finish embeding msg with the critical value of ⍴ being {rhoT}')
    img, gray, pError = enough
    #
    border = sorted(
        list(
            set(map(tuple, np.argwhere(gray == gray))) -
            set(map(tuple,
                    np.argwhere(gray[1:-1, 1:-1] == gray[1:-1, 1:-1]) + 1))))
    border = list(filter(lambda xy: invariant(img[xy]), border))
    if len(border) < 56:
        print('The size of image is too small to contain the necessary parameters')
        exit()
    for char, loc in zip(f'{rhoT:016b}' + f'{lastEc:08b}' + f'{La:016b}' + f'{N:016b}',
                         filter(lambda xy: invariant(img[xy]), border)):
        img[loc][2] = 2 * (img[loc][2] // 2) + int(char)
    print(f'=> Finish embeding parameters:\n\trhoT: {rhoT}, lastEc: {lastEc}, La: {La}, N: {N}, tagsCode: {tagsCode}')
    cv2.imwrite('./Slena.png', cv2.cvtColor(img, cv2.COLOR_RGB2BGR))

    # 提取信息
    imgRcv = cv2.imread('./Slena.png')
    imgRcv = cv2.cvtColor(imgRcv, cv2.COLOR_BGR2RGB)
    grayRcv = cvtGray(imgRcv)
    predictRcv, pErrorRcv, rhoRcv = PEs(grayRcv, imgRcv)
    print(f'=> Finish reading embeded image and calculating predication error!')
    #验证
    plt.subplot(1, 2, 2), plt.title('Modified')
    plt.hist(grayRcv.ravel(), 256)
    plt.show(block=False)
    print(f'=> Ensure the grayscale invariant: {np.all(gray == grayRcv)}')
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
    print(
        f'=> Finish extractig parameters:\n\trhoT: {rhoT}, lastEc: {lastEc}, La: {La}, N: {N}, tagsCode: {"".join([str(i) for i in tagsCode])}'
    )

    candidate = reversed([selected[:N][index] for index, value in enumerate(tagsCode) if value == 0])
    predictRcv = imgRcv.copy()
    pErrorRcv = np.zeros(imgRcv.shape)
    msgRcv = []
    for i in candidate:
        rM = np.array([imgRcv[i[0] + 1, i[1], 0], imgRcv[i[0], i[1] + 1, 0],
                       imgRcv[i[0] + 1, i[1] + 1, 0]]).reshape(3, 1)
        bM = np.array([imgRcv[i[0] + 1, i[1], 2], imgRcv[i[0], i[1] + 1, 2],
                       imgRcv[i[0] + 1, i[1] + 1, 2]]).reshape(3, 1)
        grM = np.array([grayRcv[i[0] + 1, i[1]], grayRcv[i[0], i[1] + 1], grayRcv[i[0] + 1, i[1] + 1]]).reshape(3, 1)
        X = np.mat(np.column_stack(([1] * 3, grM, grM**2)))
        predictRcv[i][0] = predictV(rM, grayRcv[i], X)
        predictRcv[i][2] = predictV(bM, grayRcv[i], X)
        
        pErrorRcv[i] = imgRcv[i] - predictRcv[i]

        msgRcv.append(int(pErrorRcv[i][0]) % 2)
        nextEc = pErrorRcv[i][2] % 2

        pErrorRcv[i] = pErrorRcv[i] // 2
        imgRcv[i] = predictRcv[i] + pErrorRcv[i]
        imgRcv[i][1] = np.round((grayRcv[i] - imgRcv[i][0] * RGB[0] - imgRcv[i][2] * RGB[2]) / RGB[1])
        if lastEc != 0:
            if np.round(np.array([imgRcv[i][0], imgRcv[i][1] + lastEc, imgRcv[i][2]]).dot(RGB)) == grayRcv[i]:
                imgRcv[i][1] += lastEc
            elif np.round(np.array([imgRcv[i][0], imgRcv[i][1] - lastEc, imgRcv[i][2]]).dot(RGB)) == grayRcv[i]:
                imgRcv[i][1] -= lastEc
        else:
            if np.round(np.array([imgRcv[i][0], imgRcv[i][1], imgRcv[i][2]]).dot(RGB)) != grayRcv[i]:
                print(f"index {i} has no matched ec")
                pass

        lastEc = abs(nextEc)
    print(f"=> Finish extracting received msg: {int(''.join([str(i) for i in list(reversed(msgRcv))]), 2)}")
    print(
        f"=>\n{bin(msg)[2:]}\n{''.join([str(i) for i in list(reversed(msgRcv))])} The msg is equal to received msg: {''.join(bin(msg)[2:]) == ''.join([str(i) for i in list(reversed(msgRcv))])}"
    )
    # plt.show()