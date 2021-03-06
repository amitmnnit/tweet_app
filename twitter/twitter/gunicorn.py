#!python
from os import environ
from gevent import monkey
monkey.patch_all()

bind = "0.0.0.0:8000"
workers = 1 # fine for dev, you probably want to increase this number in production
worker_class = "gunicorn.workers.ggevent.GeventWorker"