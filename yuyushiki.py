# -*- coding: utf-8 -*-
import atexit
from functools import reduce
from pathlib import Path

from flask import Flask, render_template, send_from_directory, request, send_file
from pymongo import Connection

app = Flask(__name__)
app.config.update(
    DEBUG=True,
)


con = Connection('localhost', 27017)
collection = con.yuyushiki.comics
atexit.register(con.close)

root = Path('data')
pages = reduce(lambda a, b:a+b, [[p for p in path.iterdir()] for path in root.iterdir()])
pages.sort()

def get_latest():
    return list(collection.find({}).sort('_id',-1).limit(1))

def find_one(path):
    return collection.find_one({'path':path})

def insert(path, script, characters, reedit, useless):
    d = {'path':path, 'script':script, 'characters':characters,
            'reedit':reedit, 'useless':useless}
    collection.insert(d)

def upsert(path, script, characters, reedit, useless):
    d = {'path':path, 'script':script, 'characters':characters,
            'reedit':reedit, 'useless':useless}
    collection.update({'path':path}, d, upsert=True) 

@app.route('/', methods=['GET', 'POST'])
def index():
    prev = False
    if request.method == 'POST':
        data = request.form
        if data.get('action') == 'prev': #前の画像に戻る
            path = data.get('path')
            prev = True
        else:
            script = data.get('script', '')
            path = data.get('path')
            characters = [] #TODO
            reedit = bool(data.get('reedit', False))
            useless = bool(data.get('useless', False))
            upsert(path, script, characters, reedit, useless)
        
        i = pages.index(Path(path))
        if prev:
            p = pages[i-1]
        else:
            p = pages[i+1]
    elif request.method == 'GET':
        latest = get_latest()
        if latest == []:
            p = pages[0]
        else:
            i = pages.index(Path(latest[0]['path']))
            p = pages[i+1]
    
    prev_data = find_one(p.as_posix())
    progress = round(collection.count() * 100 / len(pages), 2)
    return render_template('index.html', path=p, progress=progress, prev_data=prev_data)

@app.route('/data/<path:filename>')
def static_yuyushiki(filename):
    return send_from_directory(root.as_posix(), filename)

@app.route('/templates/main.js')
def load_js():
    return send_file('templates/main.js')

if __name__ == '__main__':
    app.run(host='0.0.0.0')

