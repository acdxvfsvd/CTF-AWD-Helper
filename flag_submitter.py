# -*- coding: utf-8 -*-
import requests
import json
import time

def submit_routine(flag_url, flag, flag_param, flag_method, addition_params):
    try:
        payload = dict({flag_param: flag}, **addition_params)
        if (flag_method == 'GET'):
            r = requests.get(flag_url, params = payload)
        elif (flag_method == 'POST'):
            r = requests.post(flag_url, data = payload)
        result = r.text
    except Exception as e:
        result = str(e)
    return json.dumps({'flag': flag, 'result': result, 'time': time.asctime(time.localtime(time.time()))})