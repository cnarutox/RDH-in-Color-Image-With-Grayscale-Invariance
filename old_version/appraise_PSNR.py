import numpy as np
import math


def appraise_PSNR(img1, img2):
    # img1,img2 are np.array
    img1 = img1.astype(np.float)
    img2 = img2.astype(np.float)
    L = img1.size
    mse = np.vdot(img1 - img2, img1 - img2) / L
    psnr = 10 * math.log10(255 * 255 / mse)

    return psnr


# for testing
img1 = np.array([[1, 2, 3], [2, 3, 4], [3, 4, 5]])
img2 = np.array([[2, 3, 4], [3, 4, 5], [1, 2, 3]])
print(appraise_PSNR(img1, img2))
