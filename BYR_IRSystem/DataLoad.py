#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json


# class Post:
#     def __init__(self, json_object):
#         self.title = json_object['title']
#         self.publish_time = json_object['publish_time']
#         self.author = json_object['author']
#         self.read_count = json_object['read_count']
#         self.latest_reply_time = json_object['latest_reply_time']
#         self.latest_reply_author = json_object['latest_reply_author']
#         self.link = json_object['link']
#         self.main_content = json_object['main_content']
#         self.board = json_object['board']
#         self.id = json_object['id']



def formatter_json(file_name):
    with open("./Data/" + file_name + ".json") as fp:
        line = fp.readline()
        line = line.replace('}][{', ',')
    with open("./Data/" + file_name + "_copy.json", "w") as fp:
        fp.write(line)

def modify_field(file_name):
    with open("./Data/" + file_name + ".json") as fp:
        list = json.load(fp)
        print(1)
        for i in list:
            i['title'] = i['字段1_文本']
            i.pop('字段1_文本')
            i['publish_time'] = i['字段2']
            i.pop('字段2')
            i['author'] = i['字段3_文本']
            i.pop('字段3_文本')
            i['read_count'] = i['文本']
            i.pop('文本')
            i['latest_reply_time'] = i['时间_文本']
            i.pop('时间_文本')
            i['latest_reply_author'] = i['字段4_文本']
            i.pop('字段4_文本')
            i['link'] = i['链接地址']
            i.pop('链接地址')
        with open("./Data/" + file_name + "_formatted.json", "w") as fp:
            fp.write("[")

            for i in list:
                res = json.dumps(i, ensure_ascii=False, indent=4) + "\n"
                fp.write(res)
                if i != list[-1]:
                    fp.write(",")
            fp.write("]")

def merge(file_name1, file_name2):
    with open("./Data/" + file_name1 + ".json") as fp:
        full = json.load(fp)
    with open("./Data/" + file_name2 + ".json") as fp:
        content_link = json.load(fp)
    for i in content_link:
        i['页面网址'] = i['页面网址'].replace('#!', '')
        for j in full:
            if j['link'] == i['页面网址']:
                j['main_content'] = i['字段2']
                break

    for i in full:
        if 'main_content' not in i:
            full.remove(i)
    with open("./Data/" + file_name1 + "_merge.json", "w") as fp:
        fp.write("[")

        for i in full:
            res = json.dumps(i, ensure_ascii=False, indent=4) + "\n"
            fp.write(res)
            if i != full[-1]:
                fp.write(",")
        fp.write("]")

def addBoardAndId(file_name, board):
    with open("./Data/" + file_name + ".json") as fp:
        full = json.load(fp)
        for i in full:
            i['board'] = board

            i['id'] = int(i['link'].split('/')[-1])
    with open("./Data/" + file_name + "_board.json", "w") as fp:
        fp.write("[")
        for i in full:
            res = json.dumps(i, ensure_ascii=False, indent=4) + "\n"
            fp.write(res)
            if i != full[-1]:
                fp.write(",")
        fp.write("]")

all_posts = {}
with open('./Data/飞跃重洋.json') as fp:
    temp_data = json.load(fp)
    for i in temp_data:
        all_posts[i['id']] = i


# merge('飞跃重洋_copy_formatted', '飞跃重洋帖子_copy')

