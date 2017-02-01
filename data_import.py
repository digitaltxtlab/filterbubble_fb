# -*- coding: utf-8 -*-
"""
import time, status updates and add ID for each participant
"""
import os, re
import pandas as pd
import numpy as np
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

#df_status = import_status("/home/kln/projects/bechmann/data/sample/") 
#df_status.head()
#status_df = import_status(filepath)
#status_df = status_df.reset_index()
#status_df.loc[0,'content']

# read full data frame for each participant
def folder_import(folderpath):
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

#datapath = "/home/kln/projects/bechmann/data/sample/"
#df_list, id = folder_import(datapath)

# extract status posts from folder import
def get_photo(df_list, files):
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
    return photo_df

# extract photo from folder import    
def get_status(df_list, files):
    status_df = []
    for i in range(len(df_list)):
        print files[i]
        df = df_list[i]
        status = df[df.iloc[:,2].str.contains('status')].iloc[:,[1,5]]
        status.columns = ['time', 'content']     
        filenumber = int(re.findall(r'\d+', files[i])[0]) 
        status['id'] = pd.Series((np.repeat(filenumber,np.shape(status)[0])), index = status.index)   
        cols = status.columns.tolist()
        cols = cols[-1:] + cols[:-1] 
        status_df.append(status[cols])
    status_df = pd.concat(status_df) 
    return(status_df)