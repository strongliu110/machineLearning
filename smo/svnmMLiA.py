# -*- coding: utf-8 -*-

"""
支持向量机
"""

from numpy import *

def loadDataSet(fileName):
    dataMat = []; labelMat = []
    fr = open(fileName)
    for line in fr.readlines():
        lineAttr = line.strip().split('\t')
        dataMat.append([float(lineAttr[0]), float(lineAttr[1])])
        labelMat.append(float(lineAttr[2]))
    return dataMat, labelMat

def selectJrand(i, m):
    j = i
    while (j == i):
        j = int(random.uniform(0, m))
    return j

def clipAlpha(aj, H, L):
    """剪辑aj"""
    if aj > H:
        aj = H
    if aj < L:
        aj = L
    return aj


def smoSimple(dataMatIn, classLabels, C, toler, maxIter):
    """简化版SMO算法"""
    dataMatrix = mat(dataMatIn)
    labelMat = mat(classLabels).transpose()
    b = 0
    m, n = shape(dataMatrix)
    alphas = mat(zeros((m, 1)))

    iter = 0
    while (iter < maxIter):
        alphaPairsChanged = 0
        for i in range(m):
            fXi = float(multiply(alphas, labelMat).T * (dataMatrix * dataMatrix[i, :].T)) + b
            Ei = fXi - float(labelMat[i])

            # 如果alpha可以优化，则进入优化过程
            if ((labelMat[i] * Ei < -toler) and (alphas[i] < C)) or ((labelMat[i] * Ei > toler) and (alphas[i] > 0)):
                j = selectJrand(i, m)  # 随机选择第二个alpha
                fXj = float(multiply(alphas, labelMat).T * (dataMatrix * dataMatrix[j, :].T)) + b
                Ej = fXj - float(labelMat[j])
                alphaIold = alphas[i].copy()
                alphaJold = alphas[j].copy()

                # 保证alpha在0与C之间
                if (labelMat[i] != labelMat[j]):
                    L = max(0, alphas[j] - alphas[i])
                    H = min(C, C + alphas[j] - alphas[i])
                else:
                    L = max(0, alphas[j] + alphas[i] - C)
                    H = min(C, alphas[j] + alphas[i])
                if L == H:
                    print "L==H"
                    continue

                eta = 2.0 * dataMatrix[i, :] * dataMatrix[j, :].T - \
                      dataMatrix[i, :] * dataMatrix[i, :].T - dataMatrix[j, :] * dataMatrix[j, :].T
                if eta >= 0:
                    print "eta>=0"
                    continue

                alphas[j] -= labelMat[j] * (Ei - Ej) / eta
                alphas[j] = clipAlpha(alphas[j], H, L)
                if (abs(alphas[j] - alphaJold) < 0.00001):
                    print "j not moving enough"
                    continue
                alphas[i] += labelMat[j] * labelMat[i] * (alphaJold - alphas[j])  # 对i进行修改，修改量与j相同，但方向相反

                b1 = b - Ei - labelMat[i] * (alphas[i] - alphaIold) * dataMatrix[i, :] * dataMatrix[i, :].T - \
                     labelMat[j] * (alphas[j] - alphaJold) * dataMatrix[i, :] * dataMatrix[j, :].T
                b2 = b - Ej - labelMat[i] * (alphas[i] - alphaIold) * dataMatrix[i, :] * dataMatrix[j, :].T -\
                    labelMat[j] * (alphas[j] - alphaJold) * dataMatrix[j, :] * dataMatrix[j, :].T
                if (0 < alphas[i]) and (C > alphas[i]):
                    b = b1
                elif (0 < alphas[j]) and (C > alphas[j]):
                    b = b2
                else:
                    b = (b1 + b2) / 2.0

                alphaPairsChanged += 1
                print "iter: %d i:%d, pairs changed %d" % (iter, i, alphaPairsChanged)

        if (alphaPairsChanged == 0):
            iter += 1
        else:
            iter = 0
        print "iteration number: %d" % iter
    return b, alphas

"""
dataAttr, labelAttr = loadDataSet('testSet.txt')
print labelAttr

b, alphas = smoSimple(dataAttr, labelAttr, 0.6, 0.001, 40)
print b
print alphas[alphas > 0]
shape(alphas[alphas > 0])
for i in range(100):
    if alphas[i] > 0.0:
        print dataAttr[i], labelAttr[i]
"""