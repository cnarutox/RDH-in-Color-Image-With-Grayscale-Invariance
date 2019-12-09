import numpy as np
import random
import math
import compresscoder

def addPEs(gray, cover, PER, PEB, pred_R, pred_B, sel_ind, lsb_ind, messL, D_T):
    R = np.array(float(cover[:, :, 0]))
    G = np.array(float(cover[:, :, 1]))
    B = np.array(float(cover[:, :, 2]))
    cR = 0.299
    cG = 0.587
    cB = 0.114
    (ht, wd) = G.shape
    mess = round(np.random.rand(1, messL))
    tags = np.zeros((1, wd*ht))
    ac_bit = 1
    id = 0
    tag = 0
    L_embedmess = 1

    for i in range(2, ht):
        if L_embedmess >= messL:
            break
        for j in range(2, wd):
            id += 1
            if id > len(sel_ind):
                break
            c_id = sel_ind[id]
            ii = math.floor((c_id - 1) / (ht - 2)) + 2
            jj = ((c_id - 1) % (ht - 2)) + 2

            PER[c_id] = 2 * PER[c_id] + mess(L_embedmess)
            PEB[c_id] = 2 * PEB[c_id] + ac_bit
            M_R = PER[c_id] + pred_R[c_id]
            M_B = PEB[c_id] + pred_B[c_id]
            M_G = round((gray[ii, jj] - cR * M_R - cB * M_B / cG))
            rec_G = round((gray[ii, jj] - cR * R[ii, jj] - cB * B[ii, jj]) / cG)
            ac_bit = abs(round(rec_G - G[ii, jj]))
            D = (R[ii, jj] - M_R)^2 + (G[ii, jj] - M_G)^2 + (B[ii, jj] - M_B)^2

            if max(M_R, M_G, M_B) > 255 or min(M_R, M_G, M_B) < 0 or D > D_T:
                tags[id] = 1
                #R[ii, jj] = R0
                #B[ii, jj] = B0
                #G[ii, jj] = G0
            else:
                tags[id] = 0
                R[ii, jj] = M_R
                G[ii, jj] = M_G
                B[ii, jj] = M_B
                L_embedmess = L_embedmess + 1
            if L_embedmess >= messL:
                tag = 1
                break
    
    N = id
    tags = tags[1:id]
    L_a = 0
    if len(np.unique(tags)) > 1:
        L_a = compresscoder(tags)
    else:
        L_a = 1
    count = 0
    L_a += 50
    for id in range(1, len(lsb_ind)+1):
        if id > len(lsb_ind):
            break
        c_id = sel_ind(id)
        ii = math.floor((c_id - 1) / (ht - 2)) + 2
        jj = ((c_id - 1) % (ht - 2)) + 2
        if round(cR * R[ii, jj] + cG * G[ii, jj] + cB * 2 * math.floor(B[ii, jj] / 2)) == round(cR * G[ii, jj] + cG * G[ii, jj] + cB * (2 * math.floor(B[ii, jj] / 2) + 1)):
            B[ii, jj] = 2 * math.floor(B[ii, jj] / 2) + round(np.random.rand())
            count += 1
            if count > L_a:
                break
    if count < L_a:
        tag = 0
    stego = np.array()
    stego[:, :, 1] = R
    stego[:, :, 2] = G
    stego[:, :, 3] = B

    return stego, L_embedmess, L_a, tag, N
