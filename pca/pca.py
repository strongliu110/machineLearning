# -*- coding: utf-8 -*-

"""
利用PCA来简化数据
"""

from numpy import *

def loadDataSet(fileName, delim='\t'):
    fr = open(fileName)
    stringArr = [line.strip().split(delim) for line in fr.readlines()]
    datArr = [map(float, line) for line in stringArr]
    return mat(datArr)

def pca(dataMat, topNfeat=9999999):
    """
    PCA算法
    :param dataMat: 原数据集矩阵
    :param topNfeat: 应用的N个特征
    :return:
        lowDDataMat：降维后数据集
        reconMat：新的数据集空间
    """
    meanVals = mean(dataMat, axis=0)  # 求均值
    meanRemoved = dataMat - meanVals
    covMat = cov(meanRemoved, rowvar=0)  # 协方差矩阵
    eigVals, eigVects = linalg.eig(mat(covMat))  # 求解特征值与特征向量

    eigValInd = argsort(eigVals)  # 将特征值从小到大排序
    eigValInd = eigValInd[:-(topNfeat+1):-1]
    redEigVects = eigVects[:, eigValInd]  # 保留最上面的N个特征向量

    lowDDataMat = meanRemoved * redEigVects  # 降维后的数据集
    reconMat = (lowDDataMat * redEigVects.T) + meanVals  # 新的数据集空间
    return lowDDataMat, reconMat

"""
dataMat = loadDataSet('testSet.txt')
lowDMat, reconMat = pca(dataMat, 1)

import matplotlib
import matplotlib.pyplot as plt
fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(dataMat[:, 0].flatten().A[0], dataMat[:, 1].flatten().A[0], marker='^', s=90)
ax.scatter(reconMat[:, 0].flatten().A[0], reconMat[:, 1].flatten().A[0], marker='o', s=50, c='red')
plt.show()
"""

