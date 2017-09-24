# -*- coding: utf-8 -*-

from math import *
from numpy import *

def loadDataSet():
    dataMat = []
    labelMat = []
    fr = open('testSet.txt')
    for line in fr.readlines():
        lineArr = line.strip().split()
        dataMat.append([1.0, float(lineArr[0]), float(lineArr[1])])
        labelMat.append(int(lineArr[2]))
    return dataMat, labelMat

def sigmoid(inX):
    """阶跃函数"""
    return 1.0 / (1 + exp(-inX))

def gradAscent(dataMatIn, classLabels):
    """梯度上升算法"""
    dataMatrix = mat(dataMatIn)
    labelMat = mat(classLabels).transpose()  # 矩阵转置，得到列向量
    m, n = shape(dataMatrix)  # 矩阵维数
    alpha = 0.001
    maxCycles = 500
    weights = ones((n, 1))
    for k in range(maxCycles):
        h = sigmoid(dataMatrix * weights)
        error = (labelMat - h)
        weights = weights + alpha * dataMatrix.transpose() * error
    return weights

"""
dataArr, labelMat = loadDataSet()
ret = gradAscent(dataArr, labelMat)
print ret
"""

def plotBestFit(weights):
    """画出数据集和Logistic回归最佳拟合直线的函数"""
    import matplotlib.pyplot as plt
    dataMat, labelMat = loadDataSet()
    dataArray = array(dataMat)  # list转numpy.array
    n = shape(dataArray)[0]
    xcord1 = []; ycord1 = []
    xcord2 = []; ycord2 = []
    for i in range(n):
        if int(labelMat[i]) == 1:
            xcord1.append(dataArray[i, 1])
            ycord1.append(dataArray[i, 2])
        else:
            xcord2.append(dataArray[i, 1])
            ycord2.append(dataArray[i, 2])
    fig = plt.figure()
    ax = fig.add_subplot(111)  # 画布分割为1行1列，图像画在第一块
    ax.scatter(xcord1, ycord1, s=30, c='red', marker='s')  # 绘制散点图
    ax.scatter(xcord2, ycord2, s=30, c='green')
    x = arange(-3.0, 3.0, 0.1)  # 等差数列，从-3.0到3.0，公差0.1
    y = (-weights[0] - weights[1] * x) / weights[2]  # 最佳拟合直线
    ax.plot(x, y)
    plt.xlabel('X1')
    plt.ylabel('X2')
    plt.show()

"""
dataArr, labelMat = loadDataSet()
weights = gradAscent(dataArr, labelMat)
weigthsArray = matrix.getA(weights)  # 矩阵转数组 matrix.getA()
plotBestFit(weigthsArray)
"""

def stocgradAscent0(dataMatrix, classLabels):
    """随机梯度上升算法"""
    m, n = shape(dataMatrix)
    alpha = 0.01
    weights = ones(n)
    for i in range(m):
        h = sigmoid(sum(dataMatrix[i] * weights))
        error = classLabels[i] - h
        weights = weights + alpha * error * dataMatrix[i]
    return weights

"""
dataArr, labelMat = loadDataSet()
weights = stocgradAscent0(array(dataArr), labelMat)
plotBestFit(weights)
"""

def stocGradAscent1(dataMatrix, classLabels, numIter = 150):
    """改进的随机梯度上升算法"""
    m, n = shape(dataMatrix)
    weights = ones(n)
    for j in range(numIter):
        dataIndex = range(m)
        for i in range(m):
            alpha = 4 / (1.0 + j + i) + 0.01
            randIndex = int(random.uniform(0, len(dataIndex)))
            h = sigmoid(sum(dataMatrix[randIndex] * weights))
            error = classLabels[randIndex] - h
            weights = weights + alpha * error * dataMatrix[randIndex]
            del (dataIndex[randIndex])
    return weights

"""
dataArr, labelMat = loadDataSet()
weights = stocGradAscent1(array(dataArr), labelMat)
# weights = stocGradAscent1(array(dataArr), labelMat, 500)
plotBestFit(weights)
"""