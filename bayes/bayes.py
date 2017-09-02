# -*- coding: utf-8 -*-

def loadDataSet():
    postingList = [['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
                   ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
                   ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
                   ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
                   ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
                   ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
    classVec = [0, 1, 0, 1, 0, 1]

    return postingList, classVec

def createVocabList(dataSet):
    """词表去重"""
    vocabSet = set([])

    # 创建两个集合的并集
    for document in dataSet:
        vocabSet = vocabSet | set(document)

    return list(vocabSet)

def setOfWords2Vec(vocabList, inputSet):
    """词表转换成向量，词集模型"""
    returnVec = [0] * len(vocabList)  # 创建一个其中包含元素都为0的向量

    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] = 1
        else:
            print "the word: %s is not in my Vocabulary!" % word

    return returnVec

"""
listOPosts, listClasses = loadDataSet()
myVocabList = createVocabList(list0Posts)
print myVocabList

print setOfWords2Vec(myVocabList, listOPosts[0])
print setOfWords2Vec(myVocabList, listOPosts[3])
"""

from numpy import *

def trainNB0(trainMatrix, trainCaytegory):
    numTrainDocs = len(trainMatrix)  # 样本数量
    numWords = len(trainMatrix[0])  # 特征数量
    pAbusive = sum(trainCaytegory) / float(numTrainDocs)
    p0Num = ones(numWords)
    p1Num = ones(numWords)
    p0Denom = 2.0
    p1Denom = 2.0

    for i in range(numTrainDocs):
        if trainCaytegory[i] == 1:
            p1Num += trainMatrix[i]  # 某个元素出现的次数
            p1Denom += sum(trainMatrix[i])  # 总出现次数
        else:
            p0Num += trainMatrix[i]
            p0Denom += sum(trainMatrix[i])
    p1Vect = log(p1Num / p1Denom)   # 每个元素出现的概率
    p0Vect = log(p0Num / p0Denom)

    return p0Vect, p1Vect, pAbusive


"""
listOPosts, listClasses = loadDataSet()
myVocabList = createVocabList(listOPosts)

trainMat = []
for postinDoc in listOPosts:
    wordsVec = setOfWords2Vec(myVocabList, postinDoc)
    trainMat.append(wordsVec)

p0V, p1V, pAb = trainNB0(trainMat, listClasses)
print pAb
print p0V
print p1V
"""

def classifyNB(vec2Classsify, p0Vec, p1Vec, pClass1):
    p1 = sum(vec2Classsify * p1Vec) + log(pClass1)
    p0 = sum(vec2Classsify * p0Vec) + log(1.0 - pClass1)

    if p1 > p0:
        return 1
    else:
        return 0

def testingNB():
    listOPosts, listClasses = loadDataSet()
    myVocabList = createVocabList(listOPosts)
    trainMat = []
    for postinDoc in listOPosts:
        trainMat.append(setOfWords2Vec(myVocabList, postinDoc))
    p0V, p1V, pAb = trainNB0(array(trainMat), array(listClasses))

    testEntry = ['love', 'my', 'dalmation']
    thisDoc = array(setOfWords2Vec(myVocabList, testEntry))
    print testEntry, 'classified as: ', classifyNB(thisDoc, p0V, p1V, pAb)

    testEntry = ['stupid', 'garbage']
    thisDoc = array(setOfWords2Vec(myVocabList, testEntry))
    print testEntry, 'classified as: ', classifyNB(thisDoc, p0V, p1V, pAb)

"""
testingNB()
"""

def bagOfWords2VecMN(vocabList, inputSet):
    """词表转换成向量，词袋模型"""
    returnVec = [0] * len(vocabList)  # 创建一个其中包含元素都为0的向量

    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] += 1

    return returnVec

