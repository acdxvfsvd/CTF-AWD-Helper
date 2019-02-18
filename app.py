# -*- coding: utf-8 -*-
from flask import Flask, request
from flask import render_template
from os import walk
import json
import redis

from config import celery_broker_url, celery_result_backend, redis_host, redis_port

r = redis.Redis(host=redis_host, port=redis_port)

from celery import Celery

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


app = Flask(__name__)
app.config.update(
    CELERY_BROKER_URL=celery_broker_url,
    CELERY_RESULT_BACKEND=celery_result_backend
)
celery = make_celery(app)

from flag_submitter import submit_routine

flag_url = 'http://10.10.1.1:8080/submit_flag'
flag_param = 'flag'
flag_method = 'GET'
success_keyword = 'true'
addition_params = {'token': 'feeddeadbeefcafe'}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/proxy', methods = ['GET', 'POST'])
def proxy_settings():
    global flag_url, flag_param, flag_method, addition_params, success_keyword
    if request.method == 'GET': 
        return render_template('proxy.html', 
        flag_url = flag_url, 
        flag_param = flag_param, 
        flag_method = flag_method, 
        success_keyword = success_keyword,
        addition_params = json.dumps(addition_params))
    else:
        try:
            flag_url = request.form['flag_url']
            flag_param = request.form['flag_param']
            if flag_method not in ('GET', 'POST'):
                raise Exception('Meow meow meow?')
            flag_method = request.form['flag_method']
            success_keyword = request.form['success_keyword']
            addition_params = json.loads(request.form['addition_params'])
            return render_template('proxy.html', 
            flag_url = flag_url, 
            flag_param = flag_param, 
            flag_method = flag_method, 
            addition_params = json.dumps(addition_params),
            success_keyword = success_keyword,
            status = 0)
        except:
            return render_template('proxy.html', 
            flag_url = flag_url, 
            flag_param = flag_param, 
            flag_method = flag_method, 
            addition_params = json.dumps(addition_params),
            success_keyword = success_keyword,
            status = 1)
        
@app.route('/submit_flag', methods = ['GET', 'POST'])
def submit_flag():
    global flag_url, flag_param, flag_method, addition_params
    if (request.method == 'GET'):
        return 'homura tql!'
    else:
        flag = request.form['flag']
        # flag = request.args.get('flag', '')
        do_submit.delay(flag_url, flag, flag_param, flag_method, addition_params)
        return 'pushed in the queue'

@celery.task
def do_submit(flag_url, flag, flag_param, flag_method, addition_params):
    return submit_routine(flag_url, flag, flag_param, flag_method, addition_params)

@app.route('/proxy/status')
def get_proxy_status():
    result = []
    for key in r.keys('celery-task-meta-*'):
        result.append(json.loads(json.loads(r.get(key))['result']))
    # print(result)
    result.sort(key = lambda x: x['time'], reverse = True)
    return render_template('status.html', context = result, success_keyword = success_keyword)

@app.route('/repeater')
def repeater():
    file_list = []
    for root, dirs, files in walk('./pcap'):
        for f in files:
            file_list.append(f)
    print(file_list)
    return render_template('repeater.html', files = file_list)

