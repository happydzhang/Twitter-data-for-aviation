from math import log
import operator
import string
import sys
from random import choice
import random

def calcEntropy(dataSet): 
    numEntries = len(dataSet)
    labelCounts = {}
    for featVec in dataSet: 
        currentLabel = featVec[-1]
        if currentLabel not in labelCounts.keys(): labelCounts[currentLabel] = 0
        labelCounts[currentLabel] += 1
    entropy = 0.0
    for key in labelCounts:
        prob = float(labelCounts[key])/numEntries
        entropy -= prob * log(prob,2) 
    return entropy

def splitDataSet(dataSet, i, value):        
    retDataSet = []
    for featVec in dataSet:
        if featVec[i] == value:
            reducedFeatVec = featVec[:i]     
            reducedFeatVec.extend(featVec[i+1:])
            retDataSet.append(reducedFeatVec)
    return retDataSet

def selectFeature(featurelist,dataSet,m):     # select best feature from a random subset of features  
    numFeatures = len(dataSet[0]) - 1         # size of the subset is m<<M
    index = 1
    features=[]
    for i in range(numFeatures):
        features.append(index)
        index+=1
    #print features
    randomFeatures= random.sample(featurelist,m/3+1)  # the size of subset of features here is 1/3 of all features
    #print randomFeatures
    baseEntropy = calcEntropy(dataSet)
    bestInfoGain = 0.0; bestFeature = -1
    bestGainRatio = 0.0
    for i in range(numFeatures):
        if (i in randomFeatures):
            featList = [s[i] for s in dataSet]
            uniqueVals = set(featList)      
            newEntropy = 0.0
            gainRatio=0.0
            splitInfo = 0.0
            for value in uniqueVals:
                subDataSet = splitDataSet(dataSet, i, value)
                prob = len(subDataSet)/float(len(dataSet))
                newEntropy += prob * calcEntropy(subDataSet)
                splitInfo -= prob * log(prob,2)
            infoGain = baseEntropy - newEntropy
            if splitInfo == 0.0:
                splitInfo = 0.00000000000000000001
            gainRatio = infoGain/splitInfo         
            if (gainRatio > bestGainRatio):       
                bestGainRatio = gainRatio         
                bestFeature = i
    return bestFeature,bestGainRatio                    

def majorityVote(classList):       # majority voting for the node
    classCount={}
    for vote in classList:
        if vote not in classCount.keys(): classCount[vote] = 0
        classCount[vote] += 1
    sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]

def trainTree(dataSet,labels,m,originLabels):
    
    bestFeat, infoGain = selectFeature(originLabels,dataSet,m)
    classList = [s[-1] for s in dataSet]
    if classList.count(classList[0]) == len(classList):
        return classList[0]
    if (len(dataSet[0]) == 1) or (infoGain < 0.001) or bestFeat == -1:   #threshold=0.001
        return majorityVote(classList)
    bestFeatLabel = labels[bestFeat]
    model = {bestFeatLabel:{}}
    del(labels[bestFeat])
    featValues = [s[bestFeat] for s in dataSet]
    uniqueVals = set(featValues)
    for value in uniqueVals:
        subLabels = labels[:]       
        model[bestFeatLabel][value] = trainTree(splitDataSet(dataSet, bestFeat, value),subLabels,m,originLabels)
    return model

def classify(inputTree,featLabels,testVec):
    firstStr = inputTree.keys()[0]
    secondDict = inputTree[firstStr]
    featIndex = featLabels.index(firstStr)
    key = testVec[featIndex]
    valueOfFeat = secondDict[key]
    if isinstance(valueOfFeat, dict):
        classLabel = classify(valueOfFeat, featLabels, testVec)
    else: classLabel = valueOfFeat
    return classLabel

def bootstrap(dataset):   # random sample with replacement
    output = []
    k = len(dataset)
    for i in range(k):
        output.append(choice(dataset))
    return output
    

def randomForest(train,test,k):   
    TP=0
    TN=0
    FP=0
    FN=0
    candidates=[] 
    training_set=[]
    testing_set=[]
    feature_label=[]
    feature_list=[]
    modelList=[]
    f = open(train, "r")
    for line in f:
        #' '.join(line.split())
        s=line.split()
        str1 = s[1:]
        str1.append(s[0])
        training_set.append(str1)
    f.close()
    h = open(test, "r")
    for line in h:
        #' '.join(line.split())
        s=line.split()
        testing_set.append(s)
    h.close()
     
    for i in range(k):
        feature_label=[]
        feature_list=[]
        training_set = bootstrap(training_set)
        feature_index =1
        for i in range(len(training_set[0])-1):
            feature_label.append(feature_index)
            feature_list.append(feature_index)
            feature_index+=1
        model=trainTree(training_set,feature_label,feature_index,feature_label)
        modelList.append(model)
    result= []
    for s in testing_set:
        data = s[1:]
        label= s[0]
        countPositive=0
        countNegative=0
        for i in range (k):
            
            try:
                vote= classify(modelList[i],feature_list,data)
                if vote=="-1":
                    countNegative+=1
                else:
                    countPositive+=1
            except KeyError:
                pass
        if countPositive>= countNegative:                      # majority voting for all models' results
            result.append('+1')
        elif countPositive< countNegative:
            result.append('-1')

    classLabel =  [s[0] for s in testing_set] 
    for i in range(len(classLabel)):
        if (result[i] == classLabel[i] ) and (result[i] == '+1'):
            TP+=1
        elif (result[i]  == classLabel[i]  ) and (result[i] == '-1'):
            TN+=1
        elif (result[i]  != classLabel[i]  ) and (result[i] == '+1'):
            FP+=1
        elif (result[i]  != classLabel[i]  ) and (result[i] == '-1'):
            FN+=1
    print "TP="+str(TP)+'\n'+"FN="+str(FN) +'\n' +"FP="+ str(FP)+'\n'+ "TN=" +str(TN)
    return TP,TN,FP,FN

def mean(list):
    sum =0
    for s in list:
        sum+=s
    mean = sum*1.0/len(list)
    return mean

def var(list,mean): 
    var =0
    for s in list:
        var += (s-mean)*(s-mean)
    return var
    
    
def chooseParam():  # tune parameters for random forest
    sumError=0
    errorList=[]
    meanError=0
    TPlist=[]
    TNlist=[]
    FNlist=[]
    FPlist=[]
    var =0
    for i in range(10):
        TP,TN,FP,FN=randomForest("train.txt","test.txt",100)
        TPlist.append(TP)
        TNlist.append(TN)
        FPlist.append(FP)
        FNlist.append(FN)
        error = (FP+FN)*1.0/(TP+TN+FP+FN)
        sumError+=error
        errorList.append(error)
    meanError=sumError/10.0
    print mean(TPlist)
    print mean(TNlist)
    print mean(FPlist)
    print mean(FNlist)
    print mean(errorList)
    for s in errorList:
        var += ((s-meanError)*(s-meanError))

def main(argv):
    #SimpleDecisionTree(sys.argv[1],sys.argv[2])  
    #SimpleDecisionTree("train.txt","test.txt")
    #chooseParam()
    #print var
    try:
        randomForest(sys.argv[1],sys.argv[2],5)
    except AttributeError:
        pass
    #randomForest("train3.txt","test3.txt",20)
if __name__ == '__main__' : 
    main(sys.argv)            


