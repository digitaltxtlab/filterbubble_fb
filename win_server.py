#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
run edit_dist on win server
"""

import os
import numpy as np
os.chdir('D:\\KLN\\drive\\proj\\bechmann\\filterbubble_fb\\')
import data_import as di
from data_norm import normstatus
from edit_dist import norm_edist


import time

sourcepath = 'D:\\KLN\\drive\\proj\\bechmann\\data\\sample\\'
targetpath = ''

t1 = time.time()
df_list, ids = di.folder_import(sourcepath)
df_status = di.get_status(df_list, ids)
t2 = time.time()
df_status_norm = normstatus(df_status)
print t2-t1


res =  norm_edist(df_status_norm)

np.savetxt(targetpath, res, delimiter = ',')
print 'edit distance matrix saved'

df_status_norm.head()