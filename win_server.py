#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
run edit_dist on win server
"""

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
from data_norm import normstatus
from edit_dist import norm_edist


import time


targetpath = ''

t1 = time.time()
df_list, ids = di.folder_import(sourcepath)
df_status = di.get_status(df_list, ids)
t2 = time.time()
df_status_norm = normstatus(df_status)
print t2-t1


res =  norm_edist(df_status_norm)

np.savetxt(targetpath, res, delimiter = ',')
print 'distance matrix saved'


### link comparison
df_list, files = di.folder_import(sourcepath)
link_df = di.get_link(df_list,files)
