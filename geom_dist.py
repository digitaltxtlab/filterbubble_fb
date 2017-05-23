#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
calculates post by post geometrical distance for normalized status posts from data_norm
"""
__author__  = 'KLN'


import io, os, re
import numpy as np
os.chdir(os.path.expanduser("~/Documents/proj/bechmann/filterbubble_fb"))
import data_import as di

############ vis_support module
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
def plotdist(x):
    """ histogram with normal fit """
    mu = np.mean(x)
    sigma =  np.std(x)
    n, bins, patches = plt.hist(x, 50, normed=1, facecolor='k', alpha=0.75)
    y = mlab.normpdf( bins, mu, sigma)# best normal fit
    plt.plot(bins, y, 'r--', linewidth=1)
    plt.ylabel('Probability')
    plt.grid(True)
    plt.show()
    plt.close()
############ data_norm module
## language detection for filtering
from langdetect import detect
def langlist(l, err = 'NA', target = u'da'):
    """ language detection of strings s in list l with error tag err
    return iso code for each s and logical vector for target iso"""
    lang = []
    for s in l:
        try:
            tmp = detect(s)
        except:
            tmp = err
        lang.append(tmp)
    idx = [iso == target for iso in lang]    
    return lang, idx
## preprocessing for data norm
# NLP
from nltk.stem.snowball import SnowballStemmer
def cleanlist(l):
    """ alphabetcal characters kept, unicode, danish stemming"""
    sw = io.open(os.path.expanduser('~/Documents/nlp_tool/stopwords_dk.txt'),'r',encoding = 'utf8').read().lower().split()
    stemmer = SnowballStemmer('danish', ignore_stopwords = True)
    res = []
    for string in l:
        s = re.sub(ur'(?u)\W+',' ',string)
        s = re.sub(r'\d','',s)
        s = s.lower()
        tokens = s.split()
        tokens = [token for token in tokens if token not in sw]
        tokens = [stemmer.stem(token) for token in tokens]
        #if len(tokens) != 0:
        #    s = ' '.join(tokens)
        #    res.append(s)
        s = ' '.join(tokens)
        res.append(s)
    return res
# statistics
from collections import defaultdict
def prunemin(l,minfr = 1):
    """ prune lexicon of minfr types"""
    res = []
    fr = defaultdict(int)
    tmp = [s.split() for s in l] # tokenize
    for tokens in tmp:# create word counts
        for token in tokens:
            fr[token] += 1
    for tokens in tmp:
        tout = [token for token in tokens if fr[token] >= minfr]
        #if len(tout) != 0:
            #res.append(' '.join(tout))
        res.append(' '.join(tout))
    return res


## main()
# sample
sourcepath = os.path.expanduser('~/Documents/proj/bechmann/data/export_news_feed/')
# all data
sourcepath = os.path.expanduser('~/Documents/proj/bechmann/data/org/export_news_feed/')
df_list, ids = di.folder_import(sourcepath)
df_status = di.get_status(df_list, ids)
# filter on language
if 'data_lang' not in locals():
    data_lang, idx_da = langlist(list(df_status.loc[:,'content']))
else:
    print 'language vector exists'
    
df_status = df_status.iloc[idx_da,:].reset_index()
del df_status['index']
# normalize
data = list(df_status.loc[:,'content'])
data2 = cleanlist(data)
data3 = prunemin(data2,1)
df_status['content_clean'] = data3

# delete rows with empty content_clean
idx = []
for i in range(df_status.shape[0]):
    if len(df_status.loc[i,'content_clean']) == 0:
        idx.append(i)
df_status = df_status.drop(df_status.index[idx]).reset_index()
del df_status['index']
df_status.head()


####### clustering pipeline
""" combine cosine similarity, kmeans, Ward and LDA to extract latent structure """ 
from sklearn import feature_extraction
import mpld3
import pandas as pd

data = list(df_status.loc[:,'content_clean'])
## build vector space and used TF-IDF weighting
from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer(max_df = .8, min_df = 5, \
                             use_idf=True,ngram_range = (0,1))
vspc1 = vectorizer.fit_transform(data)
terms1 = vectorizer.get_feature_names()

## document reconstruction
from scipy.sparse import find
d0idx = find(vspc1[0])[1]
for i in d0idx: print terms1[i]
print data[0]
##

## cosine distance for document similarity
from sklearn.metrics.pairwise import cosine_similarity
dist = 1 - cosine_similarity(vspc1)

## kmeans

from sklearn.cluster import KMeans
k = 2
mdl1 = KMeans(n_clusters = k)# optimize parameters
%time mdl1.fit(vspc1)
class_mdl1 = mdl1.labels_.tolist()
plotdist(class_mdl1)


df = pd.DataFrame({'content': data,'group': class_mdl1}, columns = ['content','group'])
print df['group'].value_counts()

#sort cluster centers by proximity to centroid
order_centroids = mdl1.cluster_centers_.argsort()[:, ::-1]
n = 20
print 'top %d terms pr. group' %n , '\n'
for i in range(k):
    print 'group %d content:' % i, '\n'
    for ind in order_centroids[i, :n]:
        print ' %s' % terms1[ind] + ', '
    print '-----'
len(terms1)
## MDS for vis, mds is inefficient for medium to large data sets, use pcs/simple mds instead
import matplotlib.pyplot as plt
import matplotlib as mpl

from sklearn.manifold import MDS

mds = MDS(n_components = 2, dissimilarity='precomputed', random_state = 1)
mdl2 = mds.fit_transform(dist)
xs, ys = mdl2[:,0], mdl2[:,1]

group_col = {0:'#1b9e77',1:'#d95f02'}
group_nom = {0: 'group1', 1:'group2'}

df = pd.DataFrame(dict(x=xs, y=ys, label=class_mdl1))
df.head()
groups = df.groupby('label')

# set up plot
fig, ax = plt.subplots(figsize=(9, 9)) # set size
ax.margins(0.05) # Optional, just adds 5% padding to the autoscaling

for name, group in groups:
    ax.plot(group.x, group.y, marker='o', linestyle='', ms=12, 
            label=group_nom[name], color=group_col[name], 
            mec='none')
    ax.set_aspect('auto')
    ax.tick_params(\
        axis= 'x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom='off',      # ticks along the bottom edge are off
        top='off',         # ticks along the top edge are off
        labelbottom='off')
    ax.tick_params(\
        axis= 'y',
        which='both',
        left='off',
        top='off',
        labelleft='off')
    
ax.legend(numpoints=1)  #show legend with only 1 point

# fast PCA
from sklearn.decomposition import PCA
princomp = PCA(n_components=2, random_state = 23).fit(dist)
dist2d = princomp.transform(dist)
plt.figure(figsize=(9, 9))
plt.scatter(dist2d[:,0], dist2d[:,1], c=class_mdl1, marker='o', s = 40)
plt.tick_params(axis= 'x', which='both', bottom='off', top='off', labelbottom='off')
plt.tick_params(axis= 'y', which='both', bottom='off', top='off', labelbottom='off')


## HCA, ACM, Ward on Cosine dist
from scipy.cluster.hierarchy import ward, dendrogram
%time link = ward(dist) 

fig, ax = plt.subplots(figsize=(9, 9))
ax = dendrogram(link, orientation="right");
plt.tick_params(axis= 'x', which='both', bottom='off', top='off', labelbottom='off')
plt.tight_layout()


## LDA
from gensim import corpora, models, similarities

tokens = [s.split() for s in data]

dictionary = corpora.Dictionary(tokens)
dictionary.filter_extremes(no_below=5, no_above=0.8)
bow = [dictionary.doc2bow(l) for l in tokens]

%time lda = models.LdaModel(bow, num_topics=5,id2word=dictionary,update_every=5,chunksize=10000,passes=100)

lda.show_topics()

import numpy as np

topicmat = lda.show_topics(formatted=False, num_words=10)

for topic in topicmat:
    print '-----'
    for t in topic[1]:
        print t[0]
    

dir(lda)

docrep = lda.get_document_topics(bow, minimum_probability=0)


