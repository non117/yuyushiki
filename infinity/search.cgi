#! /usr/bin/python
# -*- coding: utf-8 -*-
import cgi
import sqlite3
from functools import reduce
from jinja2 import Environment, FileSystemLoader 

conn = sqlite3.connect('yuyushiki.db', check_same_thread=False)

def get4frame():
    sql = 'select path from comics where script like "{0}%"'
    cursor = conn.cursor()
    l = cursor.execute(sql).fetchall()
    cursor.close()
    return reduce(lambda x, y: x+y,l)

def index():
    env = Environment(loader=FileSystemLoader('./', encoding='utf8'))
    tpl = env.get_template('search.html')
    params = cgi.FieldStorage().get('word','')
    #frames = get4frame()
    #html = tpl.render({'frames':frames})
    html = tpl.render({'test':params})
    print('Content-Type: text/html; charset=utf-8\n')
    print(html.encode('utf-8'))

if __name__ == '__main__':
    index()

