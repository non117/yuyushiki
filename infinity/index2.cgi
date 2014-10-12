#! /usr/bin/python
# -*- coding: utf-8 -*-
import sqlite3
from jinja2 import Environment, FileSystemLoader 

conn = sqlite3.connect('yuyushiki.db', check_same_thread=False)

def get4frame():
    sql = 'select path from comics where frameno={0} order by random() limit 1'
    cursor = conn.cursor()
    res = []
    for i in range(4):
        l = cursor.execute(sql.format(i+1)).fetchall()
        res.append(l[0][0])
    cursor.close()
    return res

def index():
    env = Environment(loader=FileSystemLoader('./', encoding='utf8'))
    tpl = env.get_template('template.html')
    frames = get4frame()
    html = tpl.render({'frames':frames})
    print('Content-Type: text/html; charset=utf-8\n')
    print(html.encode('utf-8'))

if __name__ == '__main__':
    index()

