from math import log
import operator
import string
import sys
import random





def calcEntropy(dataSet):  # calculate shannon entropy
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

def splitDataSet(dataSet, i, value):  # get subset of data after splitting 
    retDataSet = []
    for featVec in dataSet:
        if featVec[i] == value:
            reducedFeatVec = featVec[:i]     
            reducedFeatVec.extend(featVec[i+1:])
            retDataSet.append(reducedFeatVec)
    return retDataSet

def selectFeature(dataSet):   #choose the best feature based on gain ratio
    numFeatures = len(dataSet[0]) - 1     
    baseEntropy = calcEntropy(dataSet)
    bestInfoGain = 0.0; bestFeature = -1
    bestGainRatio = 0.0
    for i in range(numFeatures):       
        featList = [example[i] for example in dataSet]
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
            splitInfo = 0.00000000000000000001 # in case denominator equals zero
        gainRatio = infoGain/splitInfo         
        if (gainRatio > bestGainRatio):       
            bestGainRatio = gainRatio         
            bestFeature = i
    return bestFeature,bestGainRatio                    

def majorityVote(classList):  # majority voting for the leaves
    classCount={}
    for vote in classList:
        if vote not in classCount.keys(): classCount[vote] = 0
        classCount[vote] += 1
    sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]

def trainTree(trainSet,labels):    # create the tree using training data
    bestFeat, gainRatio = selectFeature(trainSet)
    classList = [s[-1] for s in trainSet]
    if classList.count(classList[0]) == len(classList):  # stop condition 1: all labels are the same
        return classList[0]
    if (len(trainSet[0]) == 1) or (gainRatio < 0.001) : # stop condition 2: no feature left or lower than the threshold for splitting
        return majorityVote(classList)
    bestFeatLabel = labels[bestFeat]
    model = {bestFeatLabel:{}}
    del(labels[bestFeat])
    featValues = [s[bestFeat] for s in trainSet]
    uniqueVals = set(featValues)
    for value in uniqueVals:
        subLabels = labels[:]       
        model[bestFeatLabel][value] = trainTree(splitDataSet(trainSet, bestFeat, value),subLabels) # recursively splitting the nodes
    return model

def classify(model,featLabels,testSet):  # classify unseen data
    firstStr = model.keys()[0]
    secondDict = model[firstStr]
    featIndex = featLabels.index(firstStr)
    key = testSet[featIndex]
    valueOfFeat = secondDict[key]
    if isinstance(valueOfFeat, dict):
        classLabel = classify(valueOfFeat, featLabels, testSet)
    else: classLabel = valueOfFeat
    return classLabel


def SimpleDecisionTree(train,test):
    TP=0
    TN=0
    FP=0
    FN=0
    training_set=[]
    testing_set=[]
    feature_label=[]
    feature_index =1
    feature_list=[]
    f = open(train, "r")
    for line in f:
        #' '.join(line.split())
        s=line.split()
        str1 = s[1:]
        str1.append(s[0])
        training_set.append(str1)
    f.close()
    for i in range(len(training_set[0])-1):
        feature_label.append(feature_index)
        feature_list.append(feature_index)
        feature_index+=1    
    model=trainTree(training_set,feature_label)
    h = open(test, "r")
    for line in h:
        #' '.join(line.split())
        s=line.split()
        testing_set.append(s)
    h.close()
    for s in testing_set:
        data = s[1:]
        label= s[0]
        result= classify(model,feature_list,data)
        if (result == label) and (result== '+1'):
            TP+=1
        elif (result == label) and (result== '-1'):
            TN+=1
        elif (result != label) and (result== '+1'):
            FP+=1
        elif (result != label) and (result== '-1'):
            FN+=1
    print "TP="+str(TP)+'\n'+"FN="+str(FN) +'\n' +"FP="+ str(FP)+'\n'+ "TN=" +str(TN)
    return TP,TN,FP,FN

           
def main(argv):
    SimpleDecisionTree(sys.argv[1],sys.argv[2])
    #SimpleDecisionTree("train.txt","test.txt")
    #SimpleDecisionTree("train2.txt","test2.txt")
    #SimpleDecisionTree("train3.txt","test3.txt")
if __name__ == '__main__' : 
    main(sys.argv)            


