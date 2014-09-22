from math import log
import operator
import string
import sys
import random
from textblob import TextBlob



def getFeatures(data):
    featurelist=[]
    f = open(data, "r")
    for line in f:
        feature =[]
        feature.append(line.count('@'))
        a = line.count('#OSH13')+line.count('#EAA')+line.count('#Oshkosh')+line.count('#Oshbash')\
        +line.count('#OSHbash')+line.count('#OSH10')+line.count('#OSH11')+line.count('#OSH12')\
        +line.count('#osh13')+line.count('#Osh12')+line.count('#eaa')+line.count('#AirVenture')\
        +line.count('#aviation')+line.count('#airshow')+line.count('#planes')+line.count('#osh10')
        feature.append(a)                                                                                                    
        if line.count('http')>0:
            feature.append (1)
        else:
            feature.append(0)
        decodeline = unicode(line,errors='replace')
        tweet = TextBlob(decodeline)
        #tweet = TextBlob(line)
        sentiment = tweet.sentiment
        if (sentiment[1]>=0.7) or (line.count('I')>0) or (line.count('!')>1)or (line.count('?')>0):
            feature.append("subjective")
        elif sentiment[1]<=0.3:
            feature.append("objective")
        else:
            feature.append("undecided")
        if sentiment[0]>=0:
            feature.append("positive")
        else:
            feature.append("negative")
        featurelist.append(feature)
        
        
    f.close()
    w = open('result.txt', 'w')
    for s in featurelist:
            line= str(s[0])+'\t'+str(s[1])+'\t'+str(s[2])+'\t'+s[4]+'\t'+s[3]+'\n'
            w.write(line)
        

    
    w.close( )   
           
def main():
    getFeatures("tweets.txt")
if __name__ == '__main__' :
    main()            


