#! /usr/bin/python
# -*- coding: utf-8 -*-
import sqlite3
from functools import reduce
from flask import Flask, render_template, send_from_directory, request

app = Flask(__name__)
conn = sqlite3.connect('yuyushiki.db', check_same_thread=False)

def get4frame():
    sql = 'select path from comics order by random() limit 4'
    cursor = conn.cursor()
    l = cursor.execute(sql).fetchall()
    cursor.close()
    return reduce(lambda x, y: x+y,l)

@app.route('/', methods=['GET'])
def index():
    if request.method == 'GET':
        frames = get4frame()
        return render_template('index.html', frames=frames)

@app.route('/data/<path:filename>')
def data(filename):
    return send_from_directory('data', filename)

if __name__ == '__main__':
    app.debug=True
    app.run(host='0.0.0.0')

