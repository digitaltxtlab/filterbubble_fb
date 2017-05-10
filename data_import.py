# -*- coding: utf-8 -*-
"""
import time, status updates and add ID for each participant
"""
import os, re
import pandas as pd
import numpy as np

# filepath = os.path.expanduser('~/Documents/proj/bechmann/data/sample/')
# status_df = import_status(filepath)
# status_df.loc[0,'content']

# read full data frame for each participant
def folder_import(folderpath):
    """ import list of full dataframes for each user on path"""
    files = os.listdir(folderpath)
    df_list = []
    os.chdir(folderpath)
    for file in files:
        print file
        df_list.append(pd.read_table(file, header = None, encoding = 'utf-8'))
    #for i in range(len(files)):# get id
    #    files[i] = re.sub(r'\.txt$', '', files[i])
    # files = map(int, files) # convert to integer
    return df_list, files

# df_list, ids = folder_import(filepath)

def get_photo(df_list, files):
    """ get photo posts from list of dataframes (folder_import) to dataframe with filename as id """
    photo_df = []
    for i in range(len(df_list)):
        print files[i]
        df = df = df_list[i]
        photo = df[df.iloc[:,2].str.contains('photo')].iloc[:,[1,3,7]]
        photo.columns = ['time', 'comment','image_id']
        filenumber = int(re.findall(r'\d+', files[i])[0])
        photo['id'] = pd.Series((np.repeat(filenumber,np.shape(photo)[0])), index = photo.index)
        cols = photo.columns.tolist()
        cols = cols[-1:] + cols[:-1]
        photo_df.append(photo[cols])
    photo_df = pd.concat(photo_df)
    return photo_df.reset_index().drop('index',axis=1)

#df_photo = get_photo(df_list,ids)
#df_photo.head()
#print df_p

def get_status(df_list, files):
    """ get status posts from list of dataframes (folder_import) to dataframe with filename as id """
    status_df = []
    for i in range(len(df_list)):
        #print files[i]
        df = df_list[i]
        status = df[df.iloc[:,2].str.contains('status')].iloc[:,[1,5]]
        status.columns = ['time', 'content']
        filenumber = int(re.findall(r'\d+', files[i])[0])
        status['id'] = pd.Series((np.repeat(filenumber,np.shape(status)[0])), index = status.index)
        cols = status.columns.tolist()
        cols = cols[-1:] + cols[:-1]
        status_df.append(status[cols])
    status_df = pd.concat(status_df)
    # remove nan and reset index
    idx = status_df.loc[:,'content'].isnull() == 0
    status_df = status_df.loc[idx,:].reset_index()
    return status_df.drop('index',axis=1) # remove old index

# df_status = get_status(df_list, ids)
