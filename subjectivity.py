from math import log
import operator
import string
import sys
import random
from textblob import TextBlob
from time import time
from operator import itemgetter


def subjectivity(data1,data2):
    wordlist1=[]
    wordlist2=[]
    list1=[]
    list2=[]
    featurelist1=[]
    featurelist2=[]
    porlist=[]
    f = open(data1, "r")
    
    for line in f:
        featurelist1.append(line)
        decodeline = unicode(line,errors='replace')
        tweet = TextBlob(decodeline)
        #tweet = TextBlob(line)
        por= tweet.sentiment[0]
        if por > 0.3:
            por = "positive"
        elif por <-0.3:
            por = "negative"
        else:
            por = "neutral"
        #porlist.append(por)
        sub= tweet.sentiment[1]
        if sub> 0.8:
            sub = 4
        elif sub >0.6:
            sub = 3
        elif sub >0.4:
            sub = 2
        elif sub >0.2:
            sub = 1
        else:
            sub = 0
        porlist.append(sub)
        #if tweet.sentiment[1]>0.3:
         #   count+=1
        #print tweet.words
        wordlist1.extend(tweet.words)
    #print count*1.0/len(featurelist)
   
    iList = 20
    count = {}
    for word in wordlist1:
        if count.has_key(word):
            count[word] = count[word] + 1
        else:
            count[word] = 1
    print ""
    print "Black list:" 
    print sorted(count.iteritems( ), key=itemgetter(1), reverse=True)[0:iList]
    list= sorted(count.iteritems( ), key=itemgetter(1), reverse=True)[0:iList]
    for s in list:
        list1.append(s[0])
    f.close()
    g = open(data2, "r")
    
    
    
    
    for line in g:
        featurelist2.append(line)
        decodeline = unicode(line,errors='replace')
        tweet = TextBlob(decodeline)
        #tweet = TextBlob(line)
        #print tweet.sentiment
        #if tweet.sentiment[1]>0.3:
         #   count+=1 
        wordlist2.extend(tweet.words)
    #print count*1.0/len(featurelist)
   
    iList = 20
    count = {}
    for word in wordlist2:
        if count.has_key(word):
            count[word] = count[word] + 1
        else:
            count[word] = 1
    print ""
    print "White list:" 
    print sorted(count.iteritems( ), key=itemgetter(1), reverse=True)[0:iList]
    list= sorted(count.iteritems( ), key=itemgetter(1), reverse=True)[0:iList]
    for s in list:
        list2.append(s[0])
    g.close()
    list3=[ 'pm','AirVenture', 'GoPro', 'Ford',\
            'pilot', 'hangar','Pilot','Airport','airport' \
           'Planes',  'KirbyChambliss','wing','wings','engine' \
           'aviation','Hangar','photo','Mustang','flight','flying','RT','EAAupdate','eaaupdate','Show','show','event']
    countlist=[]
    for line in featurelist2:
        decodeline = unicode(line,errors='replace')
        count=0
        for s in list3:
            if decodeline.count(s)>0:
                count+=1
        countlist.append(str(count))

    for i in list2:
        for x in list1:
            if i==x:
                print i
    #w = open('keyword.txt', 'w')
    w= open ('polarity.txt','w')
    #for s in countlist:
    for s in porlist:
            line= str(s)+'\n'
            w.write(line)
    w.close( )
        
def main():
    subjectivity("untrustworthy.txt","trustworthy.txt")
   
    
if __name__ == '__main__' :
    main()            


