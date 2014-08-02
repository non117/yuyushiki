# -*- coding: utf-8 -*-
import json
from pathlib import Path

from flask import Flask
from pymongo import Connection

app = Flask(__name__)

def get_latest():
    con = Connection('localhost', 27017)
    db = con['yuyushiki']
    return db.comics.find({}).sort('_id',-1).limit(1)

@app.route('/')
def index():
    root = Path('data')
    dirs = [path for path in root.iterdir()]
    return None

if __name__ == '__main__':
    app.debug = True
    app.run()

