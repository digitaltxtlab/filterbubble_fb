#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
normalization of data from data_import
"""
__author__  = 'KLN'

import os, re
from unidecode import unidecode
from nltk.stem.snowball import SnowballStemmer

def normstatus(df, stem = 1):
    """ Danish language normalization for status updates from data_import.get_status"""
    if stem == 1:
        stemmer = SnowballStemmer('danish', ignore_stopwords = True)
    pat = re.compile('\W+')
    for i in range(len(df)):
        s = df.loc[i,'content']
        s = s.lower()
        if stem == 1:
            tokens = s.split()
            tokens = [stemmer.stem(token) for token in tokens]
            s = ' '.join(tokens)
        s = unidecode(s)
        s = pat.sub(' ',s)
        df.loc[i,'content'] = s
    return df
"""
## main
os.chdir(os.path.expanduser("~/Documents/proj/bechmann/filterbubble_fb"))
import data_import as di

filepath = os.path.expanduser('~/Documents/proj/bechmann/data/sample/')
df_list, ids = di.folder_import(filepath)
df_status = di.get_status(df_list, ids)
df_status_norm = normstatus(df_status)







df_photo = get_photo(df_list,ids)
# grap numeric id between fbid= and &set in: fbid=10202510181169383&set
import re
l = []
for i in range(len(df_photo)):
    s = df_photo.loc[i,'image_id']
    fbid = re.findall ('fbid=(.*?)\&set', s)# normal facebook (picture) id
    if not fbid:
        fbid = re.findall('www.facebook.com\/(.*?)\/photos',s) # alternate id
    l.append(fbid)

#l

#s = df_photo.loc[5,'image_id']
#s
"""
