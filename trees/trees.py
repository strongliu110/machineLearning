# -*- coding: utf-8 -*-

from math import log

def calcShannonEnt(dataSet):
    """计算给定数据集的香农熵"""
    numEntries = len(dataSet)
    labelCounts = {}
    # 为所有可能分类创建字典
    for featVec in dataSet:
        currentLabel = featVec[-1]
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel] = 0
        labelCounts[currentLabel] += 1

    shannonEnt = 0.0
    for key in labelCounts:
        # 以2为底求对数
        prob = float(labelCounts[key]) / numEntries #  概率p(x)
        shannonEnt -= prob * log(prob, 2) #  求和，得到香农熵

    return shannonEnt

def createDataSet():
    dataSet = [[1, 1, 'yes'],
               [1, 1, 'yes'],
               [1, 0, 'no'],
               [0, 1, 'no'],
               [0, 1, 'no']]
    labels = ['no surfacing', 'flippers']
    return dataSet, labels

'''
myDat, labels = createDataSet()
print myDat
print calcShannonEnt(myDat)

myDat[0][-1] = 'maybe'
print myDat
print calcShannonEnt(myDat)
'''

def splitDataSet(dataSet, axis, value):
    # 按照给定特征划分数据集
    retDataSet = []
    for featVec in dataSet:
        if featVec[axis] == value:
            reducedFeatVec = featVec[:axis]
            reducedFeatVec.extend(featVec[axis + 1:])
            retDataSet.append(reducedFeatVec)
    return retDataSet

# '''
myDat, labels = createDataSet()
print myDat
print splitDataSet(myDat, 0, 1)
print splitDataSet(myDat, 0, 0)
# '''

def chooseBestFeatureToSplit(dataSet):
    numFeatures = len(dataSet[0]) - 1
    baseEntropy = calcShannonEnt(dataSet) #  计算无序时的信息熵
    bestInfoGain = 0.0
    bestFeature = -1
    for i in range(numFeatures):
        # 创建唯一的分类标签列表
        featList = [example[i] for example in dataSet]
        uniqueVals = set(featList)

        newEntropy = 0.0
        for value in uniqueVals:
            # 计算每种划分方式的信息熵
            subDataSet = splitDataSet(dataSet, i, value)
            prob = len(subDataSet) / float(len(dataSet))
            newEntropy += prob * calcShannonEnt(subDataSet)

        infoGain = baseEntropy - newEntropy
        if (infoGain > bestInfoGain):
            # 计算最好的信息增益
            bestInfoGain = infoGain
            bestFeature = i
    return bestFeature

'''
myDat, labels = createDataSet()
print chooseBestFeatureToSplit(myDat)
print myDat
'''






