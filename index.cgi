#!/usr/bin/python
from wsgiref.handlers import CGIHandler
from yuyushiki import app

CGIHandler().run(app)