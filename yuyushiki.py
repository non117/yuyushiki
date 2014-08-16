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
    latest = list(collection.find({}).sort('_id',-1).limit(1))
    if latest == []:
        return pages[0]
    else:
        i = pages.index(Path(latest[0]['path']))
        return pages[i+1] 

def get_tag_latest():
    latest = list(collection.find({'characters':[]}).limit(1))
    if latest == [] and collection.count() > 0:
        return get_latest()
    if latest == []:
        return pages[0]
    else:
        i = pages.index(Path(latest[0]['path']))
        return pages[i] 

def find_one(path):
    return collection.find_one({'path':path})

def upsert(path, script='', characters=[], reedit=False, useless=False):
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
            characters = []
            reedit = bool(data.get('reedit', False))
            useless = bool(data.get('useless', False))
            upsert(path, script, characters, reedit, useless)
        
        i = pages.index(Path(path))
        if i == len(pages) - 1:
            return render_template('finish.html')
        if prev:
            if i - 1 < 0:
                p = pages[i]
            else:
                p = pages[i-1]
        else:
            try:
                p = pages[i+1]
            except IndexError:
                return 'finished'
    elif request.method == 'GET':
        p = get_latest()
    
    data = find_one(p.as_posix())
    progress = round(collection.count() * 100 / len(pages), 2)
    return render_template('index.html', path=p, progress=progress, data=data)

def skip_next(data, orig):
    if data is None:
        return orig
    if data['useless']:
        data['characters'] = ['none']
        collection.update({'path':data['path']}, data, upsert=True)
        i = pages.index(Path(data['path']))
        next_data = find_one(pages[i+1].as_posix())
        if next_data is None:
            return find_one(pages[i].as_posix())
        return skip_next(next_data, orig)
    else:
        return data

def skip_prev(data, orig):
    if data['useless']:
        i = pages.index(Path(data['path']))
        prev_data = find_one(pages[i-1].as_posix())
        if prev_data is None:
            i = pages.index(Path(orig['path']))
            return find_one(pages[i+1].as_posix())
        return skip_prev(prev_data, orig)
    else:
        return data

# TODO: complete画面, pagesの最後
@app.route('/tag/', methods=['GET', 'POST'])
def tag():
    prev = False
    if request.method == 'POST':
        data = request.form
        if data.get('action') == 'prev':
            path = data.get('path')
            prev = True
        else:
            path = data.get('path')
            characters = list(filter(bool, data.getlist('characters')))
            if characters == []:
                characters.append('none')
            data = find_one(path)
            if data:
                data['characters'] = characters
                collection.update({'path':path}, data, upsert=True) 
            else:
                upsert(path, characters=characters)
        
        i = pages.index(Path(path))
        if i == len(pages) - 1:
            return render_template('finish.html')
        if prev:
            if i - 1 < 0:
                p = pages[i]
            else:
                p = pages[i-1]
        else:
            try:
                p = pages[i+1]
            except IndexError:
                return 'finished'
    elif request.method == 'GET':
        p = get_tag_latest()
    
    data = find_one(p.as_posix())
    if prev:
        data = skip_prev(data, data)
    else:
        data = skip_next(data, data)
    p = Path(data['path']) if data else p
    characters = {c:True for c in data['characters']} if data else []
    progress = round(collection.find({'characters':{'$ne':[]}}).count() * 100 / len(pages), 2)
    return render_template('tag.html', path=p, progress=progress, characters=characters)


@app.route('/data/<path:filename>')
def static_data(filename):
    return send_from_directory(root.as_posix(), filename)

@app.route('/img/<path:filename>')
def static_img(filename):
    return send_from_directory('img', filename)

@app.route('/js/main.js')
def load_js():
    return send_file('templates/main.js')

@app.route('/js/lib/<path:filename>')
def load_libs(filename):
    return send_from_directory('templates/lib', filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0')

