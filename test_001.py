#!/usr/bin/env python 2.7
# -*- coding:utf-8 -*-

import os,sys, argparse
sys.path.append("..")
import grpc
import json
import requests
import time

import helloword_pb2, helloword_pb2_grpc
from locust import Locust, TaskSet, task, events
from locust.events import EventHook


def parse_arguments():
    parser = argparse.ArgumentParser(prog='locust')
    parser.add_argument('--hatch_rate')
    parser.add_argument('--master', action='store_true')
    args, unknown = parser.parse_known_args()
    opts = vars(args)
    return args.host, int(args.clients), int(args.hatch_rate)

HOST, MAX_USERS_NUMBER, USERS_PRE_SECOND = 'www.phpserver.com:80', 1, 10

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

    class task_set(TaskSet):
        def getEnviron(self, key, default):
            if key in os.environ:
                return os.environ[key]
            else:
                return default

        def getToken(self):
            consumer_key = self.getEnviron('SELDON_OAUTH_KEY', 'oauthkey')
            consumer_secret = self.getEnviron('SELDON_OAUTH_SECRET', 'oauthsecret')
            params = {}

            params["consumer_key"] = consumer_key
            params["consumer_secret"] = consumer_secret

            url = self.oauth_endpoint + "/token"
            r = requests.get(url, params=params)
            if r.status_code == requests.codes.ok:
                j = json.loads(r.text)
                # print j
                return j["access_token"]
            else:
                print "failed call to get token"
                return None

        def on_start(self):
            # print "on start"
#            self.oauth_endpoint = self.getEnviron('SELDON_OAUTH_ENDPOINT', "http://127.0.0.1:50053")
#            self.token = self.getToken()
            self.grpc_endpoint = self.getEnviron('SELDON_GRPC_ENDPOINT', "www.phpserver.com:80")
            self.data_size = int(self.getEnviron('SELDON_DEFAULT_DATA_SIZE', "784"))

        @task
        def get_prediction(self):
            conn = grpc.insecure_channel(self.grpc_endpoint)
            client = helloword_pb2_grpc.GreeterStub(conn)
            start_time = time.time()
            kwargs = {'name': '5', 'name2': '6'}
            request = helloword_pb2.HelloRequest(**kwargs)
            try:
                reply = client.SayHello(request, 3)
            except Exception,e:
                total_time = int((time.time() - start_time) * 1000)
                events.request_failure.fire(request_type="grpc", name=HOST, response_time=total_time, exception=e)
            else:
                total_time = int((time.time() - start_time) * 1000)
                events.request_success.fire(request_type="grpc", name=HOST, response_time=total_time, response_length=0)
