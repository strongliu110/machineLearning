# -*- coding: utf-8 -*-

'''
使用Apriori算法进行关联分析
'''

from numpy import *

def loadDataSet():
    return [[1, 3, 4], [2, 3, 5], [1, 2, 3, 5], [2, 5]]


def createC1(dataSet):
    C1 = []
    for transaction in dataSet:
        for item in transaction:
            if not [item] in C1:
                C1.append([item])

    C1.sort()
    return map(frozenset, C1)  # 对C1中每个项构建一个不变集合


def scanD(D, Ck, minSupport):
    """
    :param D: 数据集
    :param Ck: 候选项集列表
    :param minSupport: 最小支持度
    :return:
    """
    ssCnt = {}
    for tid in D:
        for can in Ck:
            if can.issubset(tid):
                if not ssCnt.has_key(can):
                    ssCnt[can] = 1
                else:
                    ssCnt[can] += 1
    numItems = float(len(D))
    retList = []
    supportData = {}
    for key in ssCnt:
        support = ssCnt[key] / numItems  # 计算所有项集的支持度
        if support >= minSupport:
            retList.insert(0, key)
        supportData[key] = support
    return retList, supportData

"""
dataSet = loadDataSet()
C1 = createC1(dataSet)
D = map(set, dataSet)
L1, suppData0 = scanD(D, C1, 0.5)
"""

def aprioriGen(Lk, k):
    """
    创建候选集
    :param Lk:
    :param k:
    :return:
    """
    retList = []
    lenLk = len(Lk)
    for i in range(lenLk):
        for j in range(i+1, lenLk):
            # 前k-2个项相同时，将两个集合合并排以重
            L1 = list(Lk[i])[:k-2]; L2 = list(Lk[j])[:k-2]
            L1.sort(); L2.sort()
            if L1 == L2:
                retList.append(Lk[i] | Lk[j])
    return retList

def apriori(dataSet, minSupport = 0.5):
    """
    创建频繁项集及支持度
    :param dataSet:
    :param minSupport:
    :return:
    """
    C1 = createC1(dataSet)
    D = map(set, dataSet)
    L1, supportData = scanD(D, C1, minSupport)
    L = [L1]
    k = 2
    while (len(L[k-2]) > 0):
        Ck = aprioriGen(L[k-2], k)
        Lk, supK = scanD(D, Ck, minSupport)#scan DB to get Lk
        supportData.update(supK)
        L.append(Lk)
        k += 1
    return L, supportData

def generateRules(L, supportData, minConf=0.7):
    """
    关联规则生成函数
    :param L:频繁项集列表
    :param supportData:支持度
    :param minConf: 最小可信度阈值
    :return:
    """
    bigRuleList = []
    for i in range(1, len(L)):  # only get the sets with two or more items
        for freqSet in L[i]:
            H1 = [frozenset([item]) for item in freqSet]
            if (i > 1):
                rulesFromConseq(freqSet, H1, supportData, bigRuleList, minConf)
            else:
                calcConf(freqSet, H1, supportData, bigRuleList, minConf)
    return bigRuleList


def calcConf(freqSet, H, supportData, brl, minConf=0.7):
    """
    计算可信度
    :param freqSet:
    :param H:
    :param supportData:
    :param brl:
    :param minConf:
    :return:
    """
    prunedH = []
    for conseq in H:
        conf = supportData[freqSet] / supportData[freqSet - conseq]  # calc confidence
        if conf >= minConf:
            print freqSet - conseq, '-->', conseq, 'conf:', conf
            brl.append((freqSet - conseq, conseq, conf))
            prunedH.append(conseq)
    return prunedH


def rulesFromConseq(freqSet, H, supportData, brl, minConf=0.7):
    m = len(H[0])
    if (len(freqSet) > (m + 1)):  # try further merging
        Hmp1 = aprioriGen(H, m + 1)  # create Hm+1 new candidates
        Hmp1 = calcConf(freqSet, Hmp1, supportData, brl, minConf)
        if (len(Hmp1) > 1):  # need at least two sets to merge
            rulesFromConseq(freqSet, Hmp1, supportData, brl, minConf)

"""
dataSet = loadDataSet()
L, supportData = apriori(dataSet)
rules = generateRules(L, supportData, minConf=0.7)
# rules = generateRules(L, supportData, minConf=0.5)
"""

"""
mushDatSet = [line.split() for line in open('mushroom.dat').readlines()]
L, supportData = apriori(mushDatSet, minSupport=0.3)
for item in L[1]:
    if item.intersection('2'):
        print item

# for item in L[3]:
#     if item.intersection('2'):
#         print item
"""