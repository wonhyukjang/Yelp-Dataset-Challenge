import sqlalchemy
import nltk
from sqlalchemy import create_engine
from collections import OrderedDict
import pandas as pd
import numpy as np
from pandas import DataFrame
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk import tokenize
from nltk.corpus import stopwords
import re
import codecs
import MySQLdb
import datetime
import string
import math
import csv

def fetchFilteredData(TweetArr):
    for user in TweetArr:  
        # words = [word.lower() for word in re.findall(r'\w+',user['Tweet'])]     
        printable = set(string.printable)
        try:
            user['text'] = filter(lambda x: x in printable, user['text'])        
        except:
            user['text'] = 'none'
        word_tokens = tokenizer.tokenize(user['text'])
        user['Filtered_Tweet'] = [w.lower() for w in word_tokens]

def nameEntityRecognition(starArr):
    i = 0
    for review in starArr:
        for sent in review['sentence']:
            arr = nltk.tag.pos_tag(sent.split())
            reason = []
            for tok in arr:
                if tok[1] in POS_List:
                    reason.append(tok[0].lower())
                else:
                    if tok[0].lower() in wordPosDic:
                        resultPosDic[tok[0].lower()] += 1
                        for r in reason:
                            if r not in stop_Words:
                                try:
                                    resultPosReasonDic[r] += 1
                                except:
                                    resultPosReasonDic[r] = 1
                    elif tok[0].lower() in wordNegDic:
                        resultNegDic[tok[0].lower()] += 1
                        for r in reason:
                            if r not in stop_Words:
                                try:
                                    resultNegReasonDic[r] += 1
                                except:
                                    resultNegReasonDic[r] = 1
        i+= 1
        print i
    
def write_csv(filename, arr): 
    with open(filename,'wb') as f:
        w = csv.writer(f)
        for i in range(len(arr)):
            if i == 0:
                w.writerow(arr[i].keys())
                w.writerow(arr[i].values())
            else:
                w.writerow(arr[i].values())
                                                                      
POS_List = ['CC','CD','DT','EX','FW','IN','LS','NN','NNS','NNP',
            'NNPS','PDT','PRP','PRP$','TO','WDT','WP','WP$','WRB']
stop_Words = stopwords.words('english')
            
star0 = []     
star1 = []
star2 = []
star3 = []
star4 = []
star5 = []

wordDic = {}
wordPosDic = {}
wordNegDic = {}
tokenizer = RegexpTokenizer(r'\w+')

resultPosDic = {}
resultPosArr = []

resultNegDic = {}
resultNegArr = []

resultPosReasonDic = {}
resultPosReasonArr = []

resultNegReasonDic = {}
resultNegReasonArr = []

  
df = pd.read_csv('yelp_review_business_us_rest.csv')
df2 = pd.read_csv('PMI_PosNegYelpWordFile.csv')

Yelp = df.to_dict(orient='records')
Yelp = [x for x in Yelp]



word = df2.to_dict(orient = 'records')
word = [x for x in word]

for x in word:
    if x['SOW'] > 0:
        wordPosDic[x['word']] = x['SOW']
    elif x['SOW'] < 0:
        wordNegDic[x['word']] = x['SOW']
    wordDic[x['word']] = x['SOW']
        
fetchFilteredData(Yelp)

for review in Yelp:
    review['sentence'] = tokenize.sent_tokenize(review['text'])
    if review['stars'] == 0:
        star0.append(review)
    elif review['stars'] == 1:
        star1.append(review)
    elif review['stars'] == 2:
        star2.append(review)
    elif review['stars'] == 3:
        star3.append(review)
    elif review['stars'] == 4:
        star4.append(review)
    else:
        star5.append(review)
        
for (k,v) in wordPosDic.iteritems():
    resultPosDic[k] = 0

for (k,v) in wordNegDic.iteritems():
    resultNegDic[k] = 0
           
nameEntityRecognition(star4)

for (k,v) in resultPosDic.iteritems():
    dic = {}
    dic['word'] = k
    dic['count'] = v
    resultPosArr.append(dic)

for (k,v) in resultNegDic.iteritems():
    dic = {}
    dic['word'] = k
    dic['count'] = v
    resultNegArr.append(dic)
                                                                        
for (k,v) in resultPosReasonDic.iteritems():
    dic = {}
    dic['word'] = k
    dic['count'] = v
    resultPosReasonArr.append(dic)

for (k,v) in resultNegReasonDic.iteritems():
    dic = {}
    dic['word'] = k
    dic['count'] = v
    resultNegReasonArr.append(dic)

write_csv('star4_resultPosDic.csv',resultPosArr)
write_csv('star4_resultNegDic.csv',resultNegArr)

write_csv('star4_resultPosReasonDic.csv',resultPosReasonArr)
write_csv('star4_resultNegReasonDic.csv',resultNegReasonArr)

#with open('PMI_Senti140Revised.csv','wb') as f:
#    w = csv.writer(f)
#    for i in range(len(pmi_word_Array)):
#        if i == 0:
#            w.writerow(pmi_word_Array[i].keys())
#            w.writerow(pmi_word_Array[i].values())
#        else:
#            w.writerow(pmi_word_Array[i].values())

