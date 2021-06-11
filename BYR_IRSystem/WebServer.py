#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask_bootstrap import Bootstrap
from flask import render_template
from flask import request
import Search
import DataLoad
import logging
from logging.handlers import TimedRotatingFileHandler
import re

app = Flask(__name__)
bootstrap = Bootstrap(app)

logger = logging.getLogger()
handler = TimedRotatingFileHandler(filename='web.log', when='midnight', backupCount=0, encoding='utf-8')
handler.suffix = '%Y-%m-%d.log'
handler.extMatch = re.compile(r'^\d{4}-\d{2}-\d{2}.log')
logger.addHandler(handler)
app.logger.addHandler(handler)

@app.route('/', methods=["POST", "GET"])
def home():
    file_path = 'Home.html'
    if request.method == 'GET':

        return render_template(file_path)
    else:
        result = []
        searchResult = Search.search(str(request.form.get('key')), 5)
        for j in searchResult:
                if j in DataLoad.all_posts:
                    result.append((DataLoad.all_posts[j]))
                    print(DataLoad.all_posts[j])
        return render_template(file_path, key=str(request.form.get('key')), result=result)


@app.route('/recommend<documentid>', methods=["GET"])
def recommend(documentid):
    file_path = 'Recommend.html'
    if request.method == 'GET':
        document = DataLoad.all_posts[int(documentid)]
        results = Search.search(document['title'] + document['main_content'], 7)
        data = []
        cnt = 1
        length_max = 200
        color = ['#66D6D5', '#41777F', '#131F2C','#1AB277','#063436','#37678B']
        for j in results[1:]:
            i = DataLoad.all_posts[j]
            temp = {}
            temp['title'] = i['title']
            temp['background'] = color[cnt - 1]
            if len(i['main_content']) < length_max:
                temp['main_content'] = i['main_content']
            else:
                temp['main_content'] = i['main_content'][0:length_max]
            temp['author'] = i['author']
            temp['read_count'] = i['read_count']
            temp['link'] = i['link']
            cnt += 1
            data.append(temp)
        return render_template(file_path, result=data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
