#!/usr/bin/env python
# -*- coding: utf-8 -*-

from xml.dom.minidom import parse
import xml.dom.minidom

def get_config():
    config = {}
    DOMTree = xml.dom.minidom.parse('./config/config.xml')
    config['retrain'] = bool(DOMTree.getElementsByTagName("retrain")[0].childNodes[0].data)
    config['n_clusters'] = int(DOMTree.getElementsByTagName("k-means-n_clusters")[0].childNodes[0].data)
    config['max_iter'] = int(DOMTree.getElementsByTagName("k-means-max_iter")[0].childNodes[0].data)
    config['n_init'] = int(DOMTree.getElementsByTagName("k-means-n_init")[0].childNodes[0].data)
    return config

