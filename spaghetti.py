# -*- coding: utf-8 -*-
"""

"""

import pandas as pd
import numpy as np
import os, re
os.chdir("/home/kln/projects/bechmann/code")
import data_import as di


datapath = "/home/kln/projects/bechmann/data/sample/"
df_list, files = di.folder_import(datapath)

df_list[0].iloc[:,2].unique()
df_list[0].head()

photo_df = di.get_photo(df_list,files)
status_df = di.get_status(df_list, files)


for i in range(0,10): print photo_df.iloc[i,3]
  

########### methods for getting the unique picture id  
from unidecode import unidecode

for i in range(0,5):
    test =  photo_df.iloc[i,3]
    test = unidecode(test)
    test = test.split("/")
    for s in test:
        print s

# use regex to find .a



text = unidecode(photo_df.iloc[3,3])
print text
m = re.search('photos/(.+?)/', text)
if m:
    found = m.group(1)
print found



df = photo_df.loc[:,'image_id']
id_list = []
for l in df:
    print l
    text = l
    #m = re.search('photos/(.+?)/', text)
    m = re.search('fbid=(.+?)&set', text)    
    if m:
        id_list.append(m.group(1))
print id_list


for fbid in id_list:
    print fbid

##############################
##########################
j = 0
np.mean(dst[j])
np.std(dst[j])


t0 = status_df['tokens'][0]
t1 = status_df['tokens'][1]
t2 = status_df['tokens'][2] 
t0 = " ".join(t0)
t1 = " ".join(t1)
t2 = " ".join(t2)
distance.nlevenshtein(t1, t0, method=1)# shortest alignment
distance.nlevenshtein(t1, t2, method=1)
distance.nlevenshtein(t0, t2, method=1)
distance.nlevenshtein(t1, t0, method=2)# shortest alignment
distance.nlevenshtein(t1, t2, method=2)
distance.nlevenshtein(t0, t2, method=2)
distance.levenshtein(t1, t0)
distance.levenshtein(t1, t2)


id_u = sorted(list(set(status_df.loc[:,'id'])))
id_loop = status_df.loc[:,'id'] == id_u[0]
status_df['tokens']
##########################



id_u = list(set(status_df.loc[:,'id']))
id_bool = status_df.loc[:,'id'] == id_u[2]
s = status_df.loc[:,'content']





# average distance between 
import editdistance
# compare strings
editdistance.eval('banana', 'bahama')
# compare list of strings, normal Levenshtein is length dependent
editdistance.eval(['spam', 'egg'], ['spam', 'ham'])
editdistance.eval(['spam', 'egg'], ['ham', 'spam'])


import distance
t1 = ("de", "ci", "si", "ve")
t2 = ("de", "ri", "si", "ve")
distance.levenshtein(t1, t2)
# normalized Levenshtein
distance.nlevenshtein("abc", "acd", method=1)  # shortest alignment between the sequences is taken as factor
distance.nlevenshtein("abc", "acd", method=2)  # length of longest alignment
distance.levenshtein(t1, t2)
distance.nlevenshtein(t1, t2, method=1)# shortest alignment
distance.nlevenshtein(t1, t2, method=2)
# nomalied hamming
distance.hamming("fat", "cat")
distance.hamming("fat", "cat", normalized=True)







#########################################################
import re
text = 'gfgfdAAA1234ZZZuijjk'
m = re.search('AAA(.+?)ZZZ', text)
if m:
    found = m.group(1)
    
    
    
    