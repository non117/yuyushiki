# -*- coding: utf-8 -*-
import atexit
import json
from functools import reduce
from pathlib import Path

from flask import Flask, render_template, send_from_directory
from pymongo import Connection

app = Flask(__name__)

con = Connection('localhost', 27017)
collection = con['yuyushiki'].comics
atexit.register(con.close)

root = Path('data')
pages = reduce(lambda a, b:a+b, [[p for p in path.iterdir()] for path in root.iterdir()])

def get_latest():
    return list(collection.find({}).sort('_id',-1).limit(1))

@app.route('/')
def index():
    latest = get_latest()
    if latest == []:
        p = pages[0]
    else:
        for i, p in enumerate(pages):
            if p.as_posix() == latest['path']:
                break
        p = pages[i+1]
    return render_template('index.tpl.html', path=p)

@app.route('/data/<path:filename>')
def static_yuyushiki(filename):
    return send_from_directory(root.as_posix(), filename)

if __name__ == '__main__':
    app.debug = True
    app.run()

