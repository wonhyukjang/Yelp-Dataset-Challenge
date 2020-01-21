# -*- coding: utf-8 -*-
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
import re
import codecs
import MySQLdb
import datetime
import string
import math
import csv

def log2(x):
    return math.log(x) / math.log(2)

def PMI(word, Neutral_Frequency, Tweet_Frequency, neutral_Count, word_Count):
    if word not in Neutral_Frequency:
        return None
    else:
        return log2((Neutral_Frequency[word] * word_Count)/float(Tweet_Frequency[word] * neutral_Count))

def fetchFilteredData(TweetArr):
    for user in TweetArr:  
        # words = [word.lower() for word in re.findall(r'\w+',user['Tweet'])]     
        printable = set(string.printable)
        try:
            user['text'] = filter(lambda x: x in printable, user['text'])        
        except:
            user['text'] = 'none'
        word_tokens = tokenizer.tokenize(user['text'])
        user['Filtered_Tweet'] = [w.lower() for w in word_tokens if not w.lower() in words_List]
    
def frequency(list, dic):
    for user in list:
        for token in user['Filtered_Tweet']:
            if token not in dic:
                dic[token] = 1
            else:
                dic[token] += 1                    

def is_number(s):
    try:
        complex(s) # for int, long, float and complex
    except ValueError:
        return False
    return True

stop_Words = stopwords.words('english')

words_List = stop_Words

POS_List = ['CC','CD','DT','EX','FW','IN','LS','NN','NNS','NNP',
            'NNPS','PDT','PRP','PRP$','TO','WDT','WP','WP$','WRB']
neutral_Word = []
neutral_Word_Dic = {}

neutral_Word = []
neutral_Word_Dic = {}

pos_Word = []
pos_Word_Dic = {}

posKeyArray = []

Positive = []
Positive_Frequency = {}

Negative = []
Negative_Frequency = {}

unique_word_Array = []

tokenizer = RegexpTokenizer(r'\w+')

df = pd.read_csv('/Users/wonhyukjang/Desktop/Yelp/yelp_review_business_us_rest.csv')
Yelp = df.to_dict(orient='records')
Yelp = [x for x in Yelp]
Yelp_Frequency = {}
fetchFilteredData(Yelp)
for user in Yelp:
    if user['stars'] >= 4:
        user['sentiment'] = 1
        Positive.append(user)
    elif user['stars'] <= 3:
        user['sentiment'] = -1
        Negative.append(user)

frequency(Positive, Positive_Frequency)
frequency(Negative, Negative_Frequency)
frequency(Yelp, Yelp_Frequency)

Negative_Count = len(Negative)
Positive_Count = len(Positive)
word_Count = len(Yelp_Frequency)

storage = [{'word':key, 'count':value} for key,value in Yelp_Frequency.iteritems()]
for x in storage:
    pos =  nltk.tag.pos_tag([x['word']])
    #posArray = []
    #posArray.append(pos[0][1])
    x['POS_Tag'] = pos[0][1]
    x['PMI_Positive'] = PMI(x['word'], Positive_Frequency, Yelp_Frequency, Positive_Count, word_Count)
    x['PMI_Negative'] = PMI(x['word'], Negative_Frequency, Yelp_Frequency, Negative_Count, word_Count)
    if x['PMI_Positive'] == None and x['PMI_Negative'] == None:
        x['SOW'] = 0
    elif x['PMI_Positive'] == None:
        x['SOW'] = -x['PMI_Negative']
    elif x['PMI_Negative'] == None:
        x['SOW'] = x['PMI_Positive']
    else:
        x['SOW'] = x['PMI_Positive'] - x['PMI_Negative']
print 'finish'                                     
#1048575
#pos_Array2 = []    
    
#for user in Yelp:
#    arr = nltk.tag.pos_tag(user['text'].split())
#    for tok in arr:
#        if tok[0] not in pos_Array2 and tok[1] not in POS_List:
#            pos_Array2.append(tok[0])
#
#for x in storage:
#    if x['word'] not in pos_Array2:
#        storage.remove(x)                            
#for user in Yelp:
#    arr = nltk.tag.pos_tag(user['text'].split())
#    for tok in arr:
#        for x in storage:
#            try:
#                if x['word'] == tok[0] and tok[1] not in x['POS_Tag']:                    
#                    x['POS_Tag'].append(tok[1])
#            except:
#                    continue
#print 'complete'                
#for i in range(len(Yelp)):
#    for tag in Yelp[i]['POS_Tag']:
#        if tag in POS_List:
#            Yelp.remove(i)
#            continue
            
with open('PMI_Word.csv','wb') as f:
    w = csv.writer(f)
    for i in range(len(storage)):
        if i == 0:
            w.writerow(storage[i].keys())
            w.writerow(storage[i].values())
        else:
            w.writerow(storage[i].values())
         
      