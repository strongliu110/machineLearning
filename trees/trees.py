# -*- coding: utf-8 -*-

from math import log
import operator

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
        prob = float(labelCounts[key]) / numEntries  # 概率p(x)
        shannonEnt -= prob * log(prob, 2)  # 求和，得到香农熵

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

'''
myDat, labels = createDataSet()
print myDat
print splitDataSet(myDat, 0, 1)
print splitDataSet(myDat, 0, 0)
'''

def chooseBestFeatureToSplit(dataSet):
    numFeatures = len(dataSet[0]) - 1
    baseEntropy = calcShannonEnt(dataSet)  # 计算无序时的信息熵
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

def majorityCnt(classList):
    # 多数表决
    classCount = {}
    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote] = 0
        classCount[vote] += 1

    sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]


def createTree(dataSet, labels):
    """创建决策树"""
    classList = [example[-1] for example in dataSet]  # 列向量
    # 类别完全相同则停止继续划分
    if classList.count(classList[0]) == len(classList):
        return classList[0]

    # 遍历完所有特征时返回出现次数最多的类别
    if len(dataSet[0]) == 1:
        return majorityCnt(classList)

    bestFeat = chooseBestFeatureToSplit(dataSet)
    bestFeatLabel = labels[bestFeat]
    myTree = {bestFeatLabel: {}}

    # 得到列表包含的所有属性值
    del(labels[bestFeat])
    featValues = [example[bestFeat] for example in dataSet]
    uniqueVals = set(featValues)

    for value in uniqueVals:
        subLabels = labels[:]
        myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet, bestFeat, value), subLabels)

    return myTree

"""
mydat, labels = createdataset()
mytree = createtree(mydat, labels)
print mytree
"""

def classify(inputTree, featLabels, testVec):
    """决策树的分类函数"""
    firstStr = inputTree.keys()[0]
    secondDict = inputTree[firstStr]
    featIndex = featLabels.index(firstStr)
    for key in secondDict.keys():
        if testVec[featIndex] == key:
            if type(secondDict[key]).__name__ == "dict":
                classLabel = classify(secondDict[key], featLabels, testVec)
            else:
                classLabel = secondDict[key]

    return classLabel

"""
myDat, labels = createDataSet()
print labels
import treePlotter
myTree = treePlotter.retrieveTree(0)
print myTree
print classify(myTree, labels, [1, 0])
print classify(myTree, labels, [1, 1])
# """

def storeTree(inputTree, filename):
    """存储树"""
    import pickle
    fw = open(filename, 'w')
    pickle.dump(inputTree, fw)
    fw.close()

def grabTree(filname):
    """提取树"""
    import pickle
    fr = open(filname)
    return pickle.load(fr)

"""
import treePlotter
myTree = treePlotter.retrieveTree(0)
filename = 'classifierStorage.txt'
storeTree(myTree, filename)
print grabTree(filename)
# """

# """
fr = open("lenses.txt")
lenses = [inst.strip().split('\t') for inst in fr.readlines()]
lensesLabels = ['age', 'prescript', 'astigmatic', 'tearRate']
lensesTree = createTree(lenses, lensesLabels)
print lensesTree
import treePlotter
treePlotter.createPlot(lensesTree)
# """