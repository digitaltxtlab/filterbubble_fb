#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
calculates post by post geometrical distance for normalized status posts from data_norm
"""
__author__  = 'KLN'


import io, os, re
import numpy as np
os.chdir(os.path.expanduser("~/Documents/proj/bechmann/filterbubble_fb"))
import data_import as di

############ vis support
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
def plotdist(x):
    """ histogram with normal fit """
    mu = np.mean(x)
    sigma =  np.std(x)
    n, bins, patches = plt.hist(x, 50, normed=1, facecolor='k', alpha=0.75)
    y = mlab.normpdf( bins, mu, sigma)# best normal fit
    l = plt.plot(bins, y, 'r--', linewidth=1)
    plt.ylabel('Probability')
    plt.grid(True)
    plt.show()
    plt.close(l)
############

## language detection for filtering
from langdetect import detect
def langlist(l, err = 'NA', target = u'da'):
    """ language detection of strings s in list l with error tag err
    return iso code for each s and logical vector for target iso"""
    lang = []
    for s in l:
        try:
            tmp = detect(s)
        except:
            tmp = err
        lang.append(tmp)
    idx = [iso == target for iso in lang]    
    return lang, idx
## preprocessing for data norm
# NLP
from nltk.stem.snowball import SnowballStemmer
def cleanlist(l):
    """ alphabetcal characters kept, unicode, danish stemming"""
    sw = io.open(os.path.expanduser('~/Documents/nlp_tool/stopwords_dk.txt'),'r',encoding = 'utf8').read().lower().split()
    stemmer = SnowballStemmer('danish', ignore_stopwords = True)
    res = []
    for string in l:
        s = re.sub(ur'(?u)\W+',' ',string)
        s = re.sub(r'\d','',s)
        s = s.lower()
        tokens = s.split()
        tokens = [token for token in tokens if token not in sw]
        tokens = [stemmer.stem(token) for token in tokens]
        #if len(tokens) != 0:
        #    s = ' '.join(tokens)
        #    res.append(s)
        s = ' '.join(tokens)
        res.append(s)
    return res
# statistics
from collections import defaultdict
def prunemin(l,minfr = 1):
    """ prune lexicon of minfr types"""
    res = []
    fr = defaultdict(int)
    tmp = [s.split() for s in l] # tokenize
    for tokens in tmp:# create word counts
        for token in tokens:
            fr[token] += 1
    for tokens in tmp:
        tout = [token for token in tokens if fr[token] >= minfr]
        #if len(tout) != 0:
            #res.append(' '.join(tout))
        res.append(' '.join(tout))
    return res



## main()
sourcepath = os.path.expanduser('~/Documents/proj/bechmann/data/export_news_feed/')
df_list, ids = di.folder_import(sourcepath)
df_status = di.get_status(df_list, ids)
# filter on language
data_lang, idx_da = langlist(list(df_status.loc[:,'content']))
df_status = df_status.iloc[idx_da,:].reset_index()
del df_status['index']# delete index column
# normalize
data = list(df_status.loc[:,'content'])
data2 = cleanlist(data)
data3 = prunemin(data2,2)
df_status['content_clean'] = data3

# delete rows with empty content_clean
idx = []
for i in range(df_status.shape[0]):
    if len(df_status.loc[i,'content_clean']) == 0:
        idx.append(i)
df_status = df_status.drop(df_status.index[idx]).reset_index()

df_status.head()

























