# -*- coding: utf-8 -*-
import json
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///yuyushiki.db', echo=True)
Base = declarative_base()

class Frame(Base):
    __tablename__ = 'comics'

    path = Column(String, primary_key=True)
    script = Column(String)
    characters = Column(String)
    frameno = Column(Integer)

    def __init__(self, script, path, characters, frameno):
        self.path = path
        self.script = script
        self.characters = self.list2str(characters)
        self.frameno = frameno

    def __repr__(self):
        return self.path
        
    @staticmethod
    def list2str(l):
        return ','.join(l)

    @staticmethod
    def str2list(s):
        return s.split(',')

def get_frameno(filename):
    no = int(filename[-5])
    return no % 4 + 1

def main():
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    filepath = '../yuyushiki.json'
    db = json.load(open(filepath))
    for data in db:
        if data['useless'] or data['reedit']:
            continue
        no = get_frameno(data['path'])
        frame = Frame(data['script'], data['path'], data['characters'], no)
        session.add(frame)
    session.commit()

main()

