#!/usr/bin/env python
# -*- coding: utf-8 -*-

import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
import queue
import DataLoad
from sklearn.cluster import KMeans
from ConfigLoader import get_config
import joblib
import shelve
import numpy as np


def get_corpus():
    for i in DataLoad.all_posts.values():
        text_list.append(i['title'] + i['main_content'])
        text_list_withid.append((i['id'], i['title'] + i['main_content']))


def word_cut(text):
    return jieba.lcut(text)


def ch_en_preprocess(text):
    pattern = re.compile(r'[^\u4e00-\u9fa5a-zA-Z]')
    return re.sub(pattern, '', text)


def get_word_embedding(documents):

    for i in range(len(documents)):
        documents[i] = ch_en_preprocess(documents[i])

    documents_matrix = tfidf_vectorizer.fit_transform(documents)
    document_dense = documents_matrix.toarray()
    return document_dense


def get_max_match(query_text, documents):
    query_dense = get_word_embedding(query_text)
    comp_sim = cosine_similarity(np.array(query_dense), np.array(document_dense))
    maxIndex = 0
    maxValue = 0
    for i in range(len(comp_sim[0])):
        if comp_sim[0][i] > maxValue:
            maxValue = comp_sim[0][i]
            maxIndex = i
    if maxValue != 0:
        return documents[maxIndex]
    else:
        return ''


def get_clusters():
    config = get_config()
    kmeans = None
    if config['retrain']:
        kmeans = KMeans(n_clusters=config['n_clusters'],  max_iter=config['max_iter'], n_init=config['n_init'],
                         init='k-means++').fit(document_dense)
        labels = kmeans.labels_.tolist()
        for i in range(len(labels)):
            if labels[i] not in label_text_list_withid:
                label_text_list[labels[i]] = [text_list[i]]
                label_text_list_withid[labels[i]] = [text_list_withid[i]]
            else:
                label_text_list[labels[i]].append(text_list[i])
                label_text_list_withid[labels[i]].append(text_list_withid[i])

        joblib.dump(kmeans, './model/km_cluster_fit_result.pkl')
    else:
        kmeans = joblib.load('./model/km_cluster_fit_result.pkl')
    print("K-Means load successfully.")
    return kmeans


def get_cluster_label_by_query(query):
    return KMeansPredictor.predict(get_word_embedding(query))


def get_max_k_match(query_text, documents, k, documents_with_id):
    query_dense = get_word_embedding(query_text)
    document_dense = get_word_embedding(documents)
    comp_sim = cosine_similarity(np.array(query_dense), np.array(document_dense))
    q = queue.PriorityQueue()
    queue_size = 0
    res = []
    for i in range(len(comp_sim[0])):
        q.put((comp_sim[0][i], documents_with_id[i][0]))
        queue_size += 1
        if queue_size > k:
            queue_size -= 1
            q.get()
    while not q.empty():
        temp_elem = q.get()
        res.append((temp_elem[0], temp_elem[1]))
    res.reverse()
    return res


label_text_list = {}
label_text_list_withid = {}

text_list_withid = []
text_list = []
get_corpus()
word_list = {}
for i in text_list:
    temp = jieba.lcut(i)
    for j in temp:
        if j not in word_list:
            word_list[j] = 1

current_vocabulary = word_list.keys()
config = get_config()
#if config['retrain']:
tfidf_vectorizer = TfidfVectorizer(tokenizer=word_cut, lowercase=False, vocabulary=current_vocabulary)

# joblib.dump(tfidf_vectorizer, './model/tfidf_fit_result.pkl')
# else:
#     km_cluster = joblib.load('./model/km_cluster_fit_result.pkl')

document_dense = None
if config['retrain']:
    document_dense = get_word_embedding(text_list)
    joblib.dump(document_dense, './model/document_dense.pkl')
else:
    document_dense = joblib.load('./model/document_dense.pkl')
print("Document Load Successfully.")
KMeansPredictor = get_clusters()

