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
    return 1.0 / (1 + exp(-inX))

def gradAscent(dataMatIn, classLabels):
    dataMatrix = mat(dataMatIn)
    labelMat = mat(classLabels).transpose()  # 矩阵转置，得到列向量
    m, n = shape(dataMatrix)  # 矩阵维数
    aplha = 0.001
    maxCycles = 500
    weights = ones((n, 1))
    for k in range(maxCycles):
        z = dataMatrix * weights
        h = sigmoid(z)
        error = (labelMat - h)
        weights = weights + aplha * dataMatrix.transpose() * error
    return weights

# """
dataArr, labelMat = loadDataSet()
ret = gradAscent(dataArr, labelMat)
print ret
# """