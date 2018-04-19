#!/usr/bin/env python 2.7
# -*- coding:utf-8 -*-

import os,sys, argparse
sys.path.append("..")
import json
from hyper import HTTP20Connection
import time

from locust import Locust, TaskSet, task, events
from locust.events import EventHook


def parse_arguments():
    parser = argparse.ArgumentParser(prog='locust')
    parser.add_argument('--hatch_rate')
    parser.add_argument('--master', action='store_true')
    args, unknown = parser.parse_known_args()
    opts = vars(args)
    return args.host, int(args.clients), int(args.hatch_rate)

HOST, MAX_USERS_NUMBER, USERS_PRE_SECOND = 'http2bin.org', 1, 10

# 分布式，需要启多台压测时,有一个master，其余为slave
slaves_connect = []
slave_report = EventHook()
ALL_SLAVES_CONNECTED = True
SLAVES_NUMBER = 0
def on_my_event(client_id, data):
    global ALL_SLAVES_CONNECTED
    if not ALL_SLAVES_CONNECTED:
        slaves_connect.append(client_id)
    if len(slaves_connect) == SLAVES_NUMBER:
        print "All Slaves Connected"
        ALL_SLAVES_CONNECTED = True
#        print events.slave_report._handlers
        header = {'Content-Type': 'application/x-www-form-urlencoded'}
import resource

rsrc = resource.RLIMIT_NOFILE
soft, hard = resource.getrlimit(rsrc)
print 'RLIMIT_NOFILE soft limit starts as : ', soft

soft, hard = resource.getrlimit(rsrc)
print 'RLIMIT_NOFILE soft limit change to: ', soft

events.slave_report += on_my_event

class GrpcLocust(Locust):
    def __init__(self, *args, **kwargs):
        super(GrpcLocust, self).__init__(*args, **kwargs)


class ApiUser(GrpcLocust):
    min_wait = 0
    max_wait = 0
    stop_timeout = 100
    host = 'http://http2bin.org/'

    class task_set(TaskSet):
        def getEnviron(self, key, default):
            if key in os.environ:
                return os.environ[key]
            else:
                return default

        def on_start(self):
          print "on start"
          # self.oauth_endpoint = self.getEnviron('SELDON_OAUTH_ENDPOINT', "http://127.0.0.1:50053")
          # self.token = self.getToken()



        @task
        def get_prediction(self):
            c = HTTP20Connection('http2bin.org')
            c.request('GET', '/')
            start_time = time.time()
            try:
                resp = c.get_response()
                print resp
            except Exception,e:
                total_time = int((time.time() - start_time) * 1000)
                events.request_failure.fire(request_type="grpc", name=HOST, response_time=total_time, exception=e)
            else:
                total_time = int((time.time() - start_time) * 1000)
                events.request_success.fire(request_type="grpc", name=HOST, response_time=total_time, response_length=0)
