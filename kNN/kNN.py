# -*- coding: utf-8 -*-

'''
k-近邻算法
'''

from numpy import *
import operator
from os import listdir

def createDataSet():
    group = array([[1.0, 1.1], [1.0, 1.0], [0, 0], [0, 0.1]])
    labels = ['A', 'A', 'B', 'B']
    return group, labels

def classify0(inX, dataSet, labels, k):
    """k-近邻算法"""
    dataSetSize = dataSet.shape[0]  # 获取一维长度，即样本数量

    # 距离计算
    diffMat = tile(inX, (dataSetSize, 1)) - dataSet  # inX 一维重复1次，二维重复 dataSetSize 次
    sqDiffMat = diffMat ** 2
    sqDistances = sqDiffMat.sum(axis=1)  # 将每一行向量相加
    distances = sqDistances ** 0.5

    sortedDisIndicies = distances.argsort()  # 按从小到大索引排序

    # 选择距离最小的K个点
    classCount = {}
    for i in range(k):
        voteIlabel = labels[sortedDisIndicies[i]]
        classCount[voteIlabel] = classCount.get(voteIlabel, 0) + 1

    # 排序
    sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]

'''
group, labels = createDataSet()
print "group=%r" % group
print "labels=%r" % labels
print classify0([0, 0], group, labels, 3)
'''

def file2matrix(filename):
    """文件内容转矩阵"""
    # 得到文件行数
    fr = open(filename)
    arrarOLines = fr.readlines()
    numberOfLines = len(arrarOLines)

    # 创建返回的NumPy矩阵
    returnMat = zeros((numberOfLines, 3))

    classLabelVector = []
    index = 0
    for line in arrarOLines:
        line = line.strip()  # 移除头尾空格
        listFromLine = line.split('\t')  # 以 Tab 分割
        returnMat[index, :] = listFromLine[0: 3]
        classLabelVector.append(int(listFromLine[-1]))
        index += 1

    return returnMat, classLabelVector

'''
datingDataMat, datingLabels = file2matrix('datingTestSet2.txt')

import matplotlib
import matplotlib.pyplot as plt
from numpy import array
fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(datingDataMat[:, 1], datingDataMat[:, 2], 15.0 * array(datingLabels), 15.0 * array(datingLabels))
plt.show()
'''

def autoNorm(dataSet):
    """归一化特征值"""
    minVals = dataSet.min(0)  # 取出数据集中的最小值
    maxVals = dataSet.max(0)  # 取出数据集中的最大值
    ranges = maxVals - minVals  # 计算取值范围
    normDataSet = zeros(shape(dataSet))  # 初始化一个矩阵，该矩阵和所给数据集维度相同用于存放归一化之后的数据
    m = dataSet.shape[0]  # 取出数据集的行数
    normDataSet = dataSet - tile(minVals, (m, 1))  # 这里tile()函数创建了一个以min_value为值的m行列向量
    normDataSet = normDataSet / tile(ranges, (m, 1))  # 特征值相除得到归一化后的数值
    return normDataSet, ranges, minVals

'''
datingDataMat, datingLabels = file2matrix('datingTestSet2.txt')
normMat, ranges, minVals = autoNorm(datingDataMat)
print "normMat=%r" % normMat
print "ranges=%r" % ranges
print "minVals=%r" % minVals
'''

def datingClassTest():
    """分类器针对约会网站的测试代码"""
    hoRatio = 0.10 # 测试样本占比
    datingDataMat, datingLabels = file2matrix('datingTestSet.txt')
    normMat, ranges, minVals = autoNorm(datingDataMat)
    m = normMat.shape[0]
    numTestVecs = int(m * hoRatio)
    errorCount = 0.0
    for i in range(numTestVecs):
        classifierResult = classify0(normMat[i, :], normMat[numTestVecs:m, :], datingLabels[numTestVecs:m], 3)
        print  "the classifer came back with: %d, thr real answer is: %d" \
               %(classifierResult, datingLabels[i])
        if (classifierResult != datingLabels[i]):
            errorCount += 1.0

    print "the total error rate is: %f" % (errorCount / float(numTestVecs))

'''
datingClassTest()
'''

def classifyPerson():
    """约会网站预测函数"""
    resultList = ['not at all', 'in small doses', 'in large doses']
    # percentTats = float(raw_input("percentage of time spent playing video games?"))
    # ffMiles = float(raw_input("frequent flier miles earned per year?"))
    # iceCream = float(raw_input("liters of ice cream consumed per year?"))

    percentTats = 10
    ffMiles = 10000
    iceCream = 0.5
    datingDataMat, datingLabels = file2matrix('datingTestSet2.txt')
    normMat, ranges, minVals = autoNorm(datingDataMat)
    inArr = array([ffMiles, percentTats, iceCream])
    classifierResult = classify0((inArr - minVals) / ranges, normMat, datingLabels, 3)
    print "You will probably like this person: ", resultList[classifierResult - 1]

'''
classifyPerson()
'''

def img2vector(filename):
    """图像转向量"""
    returnVect = zeros((1, 1024))
    fr = open(filename)
    for i in range(32):
        lineStr = fr.readline()
        for j in range(32):
            returnVect[0, 32 * i + j] = int(lineStr[j])

    return returnVect

def handwritingClassTest():
    """手写数字识别系统测试"""
    hwLabels = []
    # 获取目录内容
    trainingFileList = listdir('trainingDigits')
    m = len(trainingFileList)
    trainingMat = zeros((m, 1024))
    for i in range(m):
        # 从文件名解析分类数字
        fileNameStr = trainingFileList[i]
        fileStr = fileNameStr.split('.')[0]
        classNumStr = int(fileStr.split('_')[0])

        hwLabels.append(classNumStr)
        trainingMat[i, :] = img2vector('trainingDigits/%s' % fileNameStr)

    testFileList = listdir('testDigits')
    errorCount = 0.0
    mTest = len(testFileList)
    for i in range(mTest):
        fileNameStr = testFileList[i]
        fileStr = fileNameStr.split('.')[0]
        classNumStr = int(fileStr.split('_')[0])

        vectorUnderTest = img2vector('testDigits/%s' % fileNameStr)
        classifierResult = classify0(vectorUnderTest, trainingMat, hwLabels, 3)
        print "the classifier came back with: %d, the real answer is: %d" % (classifierResult, classNumStr)
        if (classifierResult != classNumStr):
            errorCount += 1.0

    print "\n the total number of errors is: %d" % errorCount
    print "\n the total error rate is: %f " % (errorCount / float(mTest))

'''
handwritingClassTest()
'''