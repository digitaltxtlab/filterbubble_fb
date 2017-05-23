#!/usr/bin/env python2
# -*- coding: utf-8 -*-
""" match/no match for each link to all other links"""
import os, platform
import numpy as np
os_name = platform.system()
if os_name == 'Windows':
    os.chdir('D:\\KLN\\drive\\proj\\bechmann\\filterbubble_fb')
    sourcepath = 'D:\\KLN\\drive\\proj\\bechmann\\data\\sample\\'
else:
    os.chdir(os.path.expanduser("~/Documents/proj/bechmann/filterbubble_fb"))
    sourcepath = os.path.expanduser('~/Documents/proj/bechmann/data/sample/')
import data_import as di

### link comparison
def link_dist(df):
    ids = sorted(list(set(df.id)))
    res = []
    for i in range(len(ids)):
        if i == len(ids)-1:
            break
        else:
            print 'source', ids[i]
            source = df.loc[df.id == ids[i],'content']
            for ii in range(i+1,len(ids)):
                target = df.loc[df.id == ids[ii],'content']
                rawlist = []
                for s in source:
                    raw = sum(s == target)
                    rawlist.append(raw)
                res.append([ids[i], ids[ii], sum(rawlist), len(source)])
    return np.vstack(res)


# main()
df_list, files = di.folder_import(sourcepath)
link_df = di.get_link(df_list,files)

foobar = di.get_link(df_list,files)
test = link_dist(foobar)
print test
