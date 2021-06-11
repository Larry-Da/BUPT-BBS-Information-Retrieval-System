#!/usr/bin/env python
# -*- coding: utf-8 -*-

import TFIDF
import threading
import time
import heapq
THREAD_NUM = 5
resQ = []


def search(key: str, k):

    label = TFIDF.get_cluster_label_by_query([key])[0]
    corpus = TFIDF.label_text_list[label]
    corpus_with_id = TFIDF.label_text_list_withid[label]

    class ThreadOfSearch(threading.Thread):
        def __init__(self, key, corpus, k, corpus_with_id):
            threading.Thread.__init__(self)
            self.key = key
            self.corpus = corpus
            self.k = k
            self.corpus_with_id = corpus_with_id

        def run(self):
            temp_res = TFIDF.get_max_k_match([self.key], self.corpus, self.k, self.corpus_with_id)
            for i in range(len(temp_res)):
                heapq.heappush(resQ, temp_res[i])
                if len(resQ) > k:
                    heapq.heappop(resQ)

    threads = []
    for i in range(THREAD_NUM):
        corpus_num = len(corpus) // THREAD_NUM

        threads.append(ThreadOfSearch(key, corpus[i*corpus_num:(i+1)*corpus_num], k, corpus_with_id[i*corpus_num:(i+1)*corpus_num]))
    if THREAD_NUM * corpus_num < len(corpus):
        threads.append(ThreadOfSearch(key, corpus[THREAD_NUM * corpus_num:], k, corpus_with_id[THREAD_NUM * corpus_num:]))

    t1 = time.time()

    for i in threads:
        i.start()

    for i in threads:
        i.join()
    t2 = time.time()
    res = []
    while not len(resQ) == 0:
        temp_elem = heapq.heappop(resQ)
        res.append(temp_elem[1])
    res.reverse()
    print("search time" + str(t2 - t1))
    return res

