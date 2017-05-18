#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
calculates post by post normalized edit distance for for normalized status posts from data_norm
"""
__author__  = 'KLN'

import os, distance, platform
import numpy as np

os_name = platform.system()
if os_name == 'Windows':
    os.chdir('D:\\KLN\\drive\\proj\\bechmann\\filterbubble_fb')
else:
    os.chdir(os.path.expanduser("~/Documents/proj/bechmann/filterbubble_fb"))
import data_import as di
from data_norm import normstatus

def main():
    os_name = platform.system()
    if os_name == 'Windows':
        sourcepath = '<your filepath there>'
        targetpath = '<your filepath there>'+'edit_dist.csv'
    else:
        sourcepath = os.path.expanduser('~/Documents/proj/bechmann/data/sample/')
        targetpath = os.path.expanduser('~/Documents/proj/bechmann/data/edit_dist_v2.csv')
    df_list, ids = di.folder_import(sourcepath)
    df_status = di.get_status(df_list, ids)
    df_status_norm = normstatus(df_status)
    res =  norm_edist(df_status_norm)
    np.savetxt(targetpath, res, delimiter = ',')
    print 'edit distance matrix saved'

def norm_edist(df):
    id_u = sorted(list(set(df.loc[:,'id'])))
    srcs_l = []
    for idx in range(0,len(id_u)):
        if idx == len(id_u)-1:
            break
        else:
            print 'source', id_u[idx]
            id_bool = df.loc[:,'id'] == id_u[idx]
            src = df.loc[:,'content'][id_bool]
            src_l = []
            i = 0
            for s in src:
                i += 1
                res_mat = np.zeros((len(id_u)-(idx+1),5))
                ii = 0
                for iii in range(idx+1,len(id_u)):
                    trgt = df.loc[:,'content'][df.loc[:,'id'] == id_u[iii]]
                    d = []
                    for t in trgt:
                        d.append(distance.nlevenshtein(s, t, method=1))
                    res_mat[ii,0] = i
                    res_mat[ii,1] = id_u[idx]
                    res_mat[ii,2] = id_u[iii]
                    res_mat[ii,3] = np.min(d)
                    res_mat[ii,4] = np.std(d)
                    ii += 1
                src_l.append(res_mat)
                src_mat = np.vstack(src_l)
            srcs_l.append(src_mat)
    srcs_mat = np.vstack(srcs_l)
    return srcs_mat

if __name__ == '__main__':
    main()
