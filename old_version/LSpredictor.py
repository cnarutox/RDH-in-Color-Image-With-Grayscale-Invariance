import numpy as np


'''
代码涉及部分
Ⅲ. PROPOSED SCHEME
B. Polynomial Predictor Based on Gray Version(基于灰色版本的多项式预测器)

生成一个具有清晰直方图的序列作为RDH的宿主序列
'''

def LSpredictor(x, y, ref_value):
    n = len(x)
    nn = min(len(np.unique(x)), len(np.unique(y)))
    k = max(nn - 1, 0)
    X = np.zeros([n, k + 1])
    X0 = np.zeros(k + 1)
    for i in range(n):
        for j in range(k + 1):
            X[i][j] = x[i] ** j
            if i == 0:
                X0[j] = ref_value ** j
    
    # 找到最佳多项式系数
    A = np.linalg.inv(X.T.dot(X)).dot(X.T).dot(np.array([y]).T)
    # 将预测结果限制再r(i+1,j)和r(i,j+1)之间
    pred_value = np.round(X0.dot(A))
    result = pred_value[0]
    if pred_value > max(y[0], y[1]):
        result = max(y[0], y[1])
    if pred_value < min(y[0], y[1]):
        result = min(y[0], y[1])
    return result
