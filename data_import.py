# -*- coding: utf-8 -*-
"""
import time, status updates and add ID for each participant
"""
import os, re
import pandas as pd
import numpy as np

def folder_import(folderpath):
    """ import list of dataframes for each user on path"""
    files = os.listdir(folderpath)
    df_list = []
    os.chdir(folderpath)
    for file in files:
        print file
        df_list.append(pd.read_table(file, header = None, encoding = 'utf-8', quoting=3))
    #for i in range(len(files)):# get id
    #    files[i] = re.sub(r'\.txt$', '', files[i])
    # files = map(int, files) # convert to integer
    return df_list, files

def get_photo(df_list, files):
    """ get photo posts from list of dataframes (folder_import) to dataframe with filename as id """
    photo_df = []
    for i in range(len(df_list)):
        print files[i]
        df = df_list[i]
        photo = df[df.iloc[:,2].str.contains('photo')].iloc[:,[1,3,7]]
        photo.columns = ['time', 'comment','image_id']
        filenumber = int(re.findall(r'\d+', files[i])[0])
        photo['id'] = pd.Series((np.repeat(filenumber,np.shape(photo)[0])), index = photo.index)
        cols = photo.columns.tolist()
        cols = cols[-1:] + cols[:-1]
        photo_df.append(photo[cols])
    photo_df = pd.concat(photo_df)
    return photo_df.reset_index().drop('index',axis=1)

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

def get_link(df_list, files):
    """ get links from each post and remove redundant characters"""
    pats = [re.compile(s) for s in ['http://','https://','www.']]
    link_df = []
    for i in range(len(df_list)):
        df = df_list[i]
        link  = df[df.iloc[:,2].str.contains('link')].iloc[:,[1,3,7]]
        link.columns = ['time','origin','content']
        idx = pd.isnull(link.origin) != True
        link = link.loc[idx,['time','content']]
        for ii in range(len(link.content)):
            s = link.content.iloc[ii]
            for pat in pats:
                s = pat.sub('',s)
                link.content.iloc[ii] = s
        filenumber = int(re.findall(r'\d+', files[i])[0])
        link['id'] = pd.Series((np.repeat(filenumber,np.shape(link)[0])), index = link.index)
        cols = link.columns.tolist()
        cols = cols[-1:] + cols[:-1]
        link_df.append(link[cols])
    link_df = pd.concat(link_df)
    link_df = link_df.reset_index()
    return link_df.drop('index',axis = 1)
