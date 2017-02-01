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








#########################################################
import re
text = 'gfgfdAAA1234ZZZuijjk'
m = re.search('AAA(.+?)ZZZ', text)
if m:
    found = m.group(1)