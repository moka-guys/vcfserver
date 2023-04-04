# file gunicorn.conf.py
# coding=utf-8

import os
# import multiprocessing

_LOGS = '/logs'
errorlog = os.path.join(_LOGS, 'vcfserver_error.log')
accesslog = os.path.join(_LOGS, 'vcfserver_access.log')
loglevel = 'info'
bind = '0.0.0.0:5000'
workers = 1  # multiprocessing.cpu_count() * 2 + 1
timeout = 30  # timeout 30 seconds
keepalive = 60 * 60  # keep connections alive for 1 hour
capture_output = True
worker_tmp_dir = '/dev/shm'  # use /dev/shm to prevent worker timeouts
worker_class = 'gthread'  # use gthread to prevent worker timeouts
