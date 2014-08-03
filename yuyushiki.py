# -*- coding: utf-8 -*-
import atexit
from functools import reduce
from pathlib import Path

from flask import Flask, render_template, send_from_directory, request
from pymongo import Connection

app = Flask(__name__)

con = Connection('localhost', 27017)
collection = con.yuyushiki.comics
atexit.register(con.close)

root = Path('data')
pages = reduce(lambda a, b:a+b, [[p for p in path.iterdir()] for path in root.iterdir()])

def get_latest():
    return list(collection.find({}).sort('_id',-1).limit(1))

def find_one(path):
    return collection.find_one({'path':path})

def insert(path, script, characters, reedit, useless):
    d = {'path':path, 'script':script, 'characters':characters,
            'reedit':reedit, 'useless':useless}
    collection.insert(d)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = request.form
        script = data.get('script', '')
        path = data.get('path')
        characters = [] #TODO
        reedit = bool(data.get('reedit', False))
        useless = bool(data.get('useless', False))
        if find_one(path):
            print('commit was duplicated.')
        else:
            insert(path, script, characters, reedit, useless)
    latest = get_latest()
    if latest == []:
        p = pages[0]
    else:
        for i, p in enumerate(pages):
            if p.as_posix() == latest[0]['path']:
                break
        p = pages[i+1]
    progress = round(collection.count() * 100 / len(pages), 2)
    return render_template('index.tpl.html', path=p, progress=progress)

@app.route('/data/<path:filename>')
def static_yuyushiki(filename):
    return send_from_directory(root.as_posix(), filename)

if __name__ == '__main__':
    app.debug = True
    app.run()

