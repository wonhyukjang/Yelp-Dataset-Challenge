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
        user['text'] = filter(lambda x: x in printable, user['text'])        
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

neutral_Word = []
neutral_Word_Dic = {}

neutral_Word = []
neutral_Word_Dic = {}

pos_Word = []
pos_Word_Dic = {}

neutralkeyArray = []
posKeyArray = []

Neutral = []
Neutral_Frequency = {}

nonNeutral = []
nonNeutral_Frequency = {}

unique_word_Array = []

tokenizer = RegexpTokenizer(r'\w+')

df = pd.read_csv('yelp_academic_dataset_review.csv')
Yelp = df.to_dict(orient='records')
Yelp = [x for x in Yelp]
Yelp_Frequency = {}
fetchFilteredData(Yelp)
for user in Yelp:
    if user['stars'] >= 3 and user['stars'] <= 4:
        user['sentiment'] = 0
        Neutral.append(user)
    elif user['stars'] < 3:
        user['sentiment'] = -1
        nonNeutral.append(user)
    else:
        user['sentiment'] = 1
        nonNeutral.append(user)

frequency(Neutral, Neutral_Frequency)
frequency(nonNeutral, nonNeutral_Frequency)
frequency(Yelp, Yelp_Frequency)

nonNeutral_Count = len(nonNeutral)
neutral_Count = len(Neutral)
word_Count = 245057

storage = [{'word':key, 'count':value} for key,value in Yelp_Frequency.iteritems()]
sow_0_Storage = []
for x in storage:
    x['PMI_Neutral'] = PMI(x['word'], Neutral_Frequency, Yelp_Frequency, neutral_Count, word_Count)
    x['PMI_nonNeutral'] = PMI(x['word'], nonNeutral_Frequency, Yelp_Frequency, nonNeutral_Count, word_Count)
    if x['PMI_Neutral'] == None and x['PMI_nonNeutral'] == None:
        x['SOW'] = 0
    elif x['PMI_Neutral'] == None:
        x['SOW'] = -x['PMI_nonNeutral']
    elif x['PMI_nonNeutral'] == None:
        x['SOW'] = x['PMI_Neutral']
    else:
        x['SOW'] = x['PMI_Neutral'] - x['PMI_nonNeutral']
    pos =  nltk.tag.pos_tag([x['word']])
    x['POS_Tag'] = pos[0][1]

for x in storage:
    if len(x['word']) <= 1 or is_number(x['word']):
        storage.remove(x)

for x in storage:
    if x['SOW'] == 0:
        sow_0_Storage.append(x)
        storage.remove(x)

with open('PMI_NeutralYelp.csv','wb') as f:
    w = csv.writer(f)
    for i in range(len(storage)):
        if i == 0:
            w.writerow(storage[i].keys())
            w.writerow(storage[i].values())
        else:
            w.writerow(storage[i].values())
#1048575        