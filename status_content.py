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
#filepath = "C:\Users\Administrator\Desktop\staythefoxout\data\sample" # for win server
#filepath = "/home/kln/projects/bechmann/data/dummy_sample"# redundant dummmy
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
# remove NaN
status_df = status_df[pd.isnull(status_df['content']) != 1]
# preprocess
content = list(status_df.loc[:,'content'])
## build feature of tokenize content in df
# normalize danish unicode characters, remove non-alphabetic chars, casefold and tokenize
from unidecode import unidecode
def normtoken(s):
    if pd.isnull(s):# check for nan
        return s
    else:
        regex = re.compile('[\#\",-\.!?0-9]')# TODO: expand
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

status_df.head()
print content[2]
print status_df.loc[2,'tokens']

##########################
# calculate average distance 


# loop through source on targets
import distance, time
t1 = time.time()

id_u = sorted(list(set(status_df.loc[:,'id'])))
idx = 0# index unique id list
id_bool = status_df.loc[:,'id'] == id_u[idx]

source = status_df.loc[:,'tokens'][id_bool].reset_index()
source_ls = []
j = 0
for s in source.loc[:,'tokens']:
#for k in range(1,4):   ### debugging
    j += 1    
    s = " ".join(s) 
#    s = " ".join(source.loc[k,'tokens']) ### debugging        
    result_mat = np.zeros((len(id_u)-(idx+1),5))
    jj = 0    
    for i in range(idx+1,len(id_u)):
        #i = 2
        target = status_df.loc[:,'tokens'][status_df.loc[:,'id'] == id_u[i]].reset_index()
        d = []
        y = 0         
        for t in target.loc[:,'tokens']:
            t = " ".join(t)
            d.append(distance.nlevenshtein(s, t, method=1))
            y += 1; print y
        # result = [np.min(d), np.std(d)]
        # print result
        result_mat[jj,0] = j # index for s (source post)
        result_mat[jj,1] = id_u[idx] # source name
        result_mat[jj,2] = id_u[i] # target name
        result_mat[jj,3] = np.min(d) # minimum distance between posts
        result_mat[jj,4] = np.std(d) # sd in distances
        jj += 1
    source_ls.append(result_mat)    
    source_mat = np.vstack(source_ls) # unstack list of arrays
print time.time() - t1

### loop over source in sources on target in targets
import distance, time
t1 = time.time()

id_u = sorted(list(set(status_df.loc[:,'id'])))
idx = 0# index unique id list
id_bool = status_df.loc[:,'id'] == id_u[idx]
sources_ls = []
for idx in range(0, len(id_u)):
    print id_u[idx]
    if idx == len(id_u)-1: break # break when no target left in targets
    id_bool = status_df.loc[:,'id'] == id_u[idx]
    source = status_df.loc[:,'tokens'][id_bool].reset_index()
    source_ls = []
    j = 0
    for s in source.loc[:,'tokens']:
    #for k in range(1,4):   ### debugging
        j += 1        
        s = " ".join(s) 
        #s = " ".join(source.loc[k,'tokens']) ### debugging        
        result_mat = np.zeros((len(id_u)-(idx+1),5))
        jj = 0
        for i in range(idx+1,len(id_u)):
            #i = 2
            target = status_df.loc[:,'tokens'][status_df.loc[:,'id'] == id_u[i]].reset_index()
            d = []
            y = 0
            for t in target.loc[:,'tokens']:
                t = " ".join(t)
                d.append(distance.nlevenshtein(s, t, method=1))
                y += 1#; print y
            result_mat[jj,0] = j
            result_mat[jj,1] = id_u[idx]
            result_mat[jj,2] = id_u[i]
            result_mat[jj,3] = np.min(d)
            result_mat[jj,4] = np.std(d)
            jj += 1
        source_ls.append(result_mat)    
        source_mat = np.vstack(source_ls) # unstack list of arrays
    sources_ls.append(source_mat)
    
sources_mat = np.vstack(sources_ls)    
timeused = time.time() - t1
print timeused