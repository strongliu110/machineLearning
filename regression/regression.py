# -*- coding: utf-8 -*-

"""

"""

from numpy import *

def loadDataSet(fileName):
    numFeat = len(open(fileName).readline().split('\t')) - 1
    dataMat = []; labelMat = []
    fr = open(fileName)
    for line in fr.readlines():
        lineArr = []
        curLine = line.strip().split('\t')
        for i in range(numFeat):
            lineArr.append(float(curLine[i]))
        dataMat.append(lineArr)
        labelMat.append(float(curLine[-1]))
    return dataMat, labelMat

def standRegres(xArr, yArr):
    """
    标准回归函数
    :param xArr:
    :param yArr:
    :return:
    """
    xMat = mat(xArr); yMat = mat(yArr).T
    xTx = xMat.T * xMat
    if linalg.det(xTx) == 0.0:  # 计算行列式的值(矩阵可逆充要条件为行列式值为0)
        print "This matrix is singular, cannot do inverse"
        return
    ws = xTx.I * (xMat.T * yMat)
    # ws = linalg.solve(xTx, xMat.T * yMat)
    return ws

# """
xArr, yArr = loadDataSet('ex0.txt')
ws = standRegres(xArr, yArr)

xMat = mat(xArr)
yMat = mat(yArr)
yHat = xMat * ws  # 预测的y值

import matplotlib.pyplot as plt
fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(xMat[:, 1].flatten().A[0], yMat.T[:, 0].flatten().A[0])  # 绘制原图

xCopy = xMat.copy()
xCopy.sort(0)
yHat = xCopy * ws
ax.plot(xCopy[:, 1], yHat)  # 绘制最佳拟合直线
plt.show()

yHat = xMat * ws
print corrcoef(yHat.T, yMat)  # 相关系数

# """
