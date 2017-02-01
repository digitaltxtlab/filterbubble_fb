# -*- coding: utf-8 -*-
"""

"""

import pandas as pd
import os
os.chdir("/home/kln/projects/bechmann/code")
from data_import import import_status

# import status updates
filepath = "/home/kln/projects/bechmann/data/sample"
status_df = import_status(filepath)
status_df = status_df.reset_index()
## write status updates to txt file
# status_df.to_csv(r'/home/kln/projects/bechmann/data/status_content.txt', header=True, sep='\t', mode='w', encoding = 'utf-8', index = False)
# status_df = pd.read_csv("/home/kln/projects/bechmann/data/status_content.txt", delimiter = '\t', index_col = False)

## write status updates to json file
#status_df = status_df.reset_index()
#status_df.to_json("/home/kln/projects/bechmann/data/status_content.json")
#status_df = pd.read_json("/home/kln/projects/bechmann/data/status_content.json")
##############################################################################
import os, re
import pandas as pd
import numpy as np

filepath = "/home/kln/projects/bechmann/data/sample"
# import files as list of tables
def import_status(filepath):
    files = os.listdir(filepath)
    df_list = []
    os.chdir(filepath)
    for file in files:
        print file
        df_list.append(pd.read_table(file, header = None, encoding = 'utf-8'))
    # extract status, col1: time and col5: str content
    # add participant id from filename
    status_df = []
    for i in range(0,len(df_list)):
        df = df_list[i]
        status = df[df.iloc[:,2].str.contains('status')].iloc[:,[1,5]]
        status.columns = ['time', 'content']     
        # add participant id    
        filenumber = int(re.findall(r'\d+', files[i])[0]) 
        status['id'] = pd.Series((np.repeat(filenumber,np.shape(status)[0])), index = status.index)   
        # rearrange columns order    
        cols = status.columns.tolist()
        cols = cols[-1:] + cols[:-1] 
        # update    
        status_df.append(status[cols])
    # concatenate
    status_df = pd.concat(status_df) 
    return(status_df)
status_df = import_status(filepath)
status_df = status_df[pd.isnull(status_df['content']) != 1]

# preprocess
content = list(status_df.loc[:,'content'])
# normalize danish unicode characters, remove non-alphabetic chars, casefold and tokenize
import re 
from unidecode import unidecode
def normtoken(s):
    if pd.isnull(s):# check for nan
        return s
    else:
        regex = re.compile('[",-\.!?0-9]')
        s = unidecode(s.lower())
        s = regex.sub('', s)
    return s.split()
# normtoken for all content
contoken = []
for s in content:
    contoken.append(normtoken(s))
# stem
from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer("danish", ignore_stopwords = True)
#[stemmer.stem(w) for w in s]
for i in range(0,len(contoken)):
    token = contoken[i]
    contoken[i] = [stemmer.stem(w) for w in token] 
# update df
status_df['tokens'] = contoken
# remove nan objects
# status_df = status_df[pd.isnull(status_df['tokens']) != 1]
status_df = status_df.reset_index()



##########################
# calculate average distance 
import distance
id_u = sorted(list(set(status_df.loc[:,'id'])))
id_bool = status_df.loc[:,'id'] == id_u[0]
# loop through sources s
s = status_df.loc[:,'tokens'][id_bool].reset_index()
# loop through targets t
dst = [] # distance vector for each target
for ii in range(0+1,len(id_u)):
    print 'target: ' + str(ii)
    t = status_df.loc[:,'tokens'][status_df.loc[:,'id'] == id_u[ii]].reset_index()
    d = []
    for i in range(0,len(t)):
        # print 'update: ' + str(i)
        t1 = " ".join(s.iloc[0,1])
        t2 = " ".join(t.iloc[i,1])
        d.append(distance.nlevenshtein(t1, t2, method=1))
    dst.append(d)
    print np.mean(d), np.std(d)
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
