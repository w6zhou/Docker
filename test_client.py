import time

import grpc

import helloword_pb2, helloword_pb2_grpc


def box_unlock():
    channel = grpc.insecure_channel("%s:%s" % ('www.phpserver.com', '80'))
    stub = helloword_pb2_grpc.GreeterStub(channel)
    kwargs = {'name': '5', 'name2': '6'}
    req = helloword_pb2.HelloRequest(**kwargs)
    response = stub.SayHello(req, 30)
    print response
    return response


if __name__ == "__main__":
    # 5005152
    start = int(time.time())
    print start
    count = 0
    now = int(time.time())
    while True:
        box_unlock()
        count = count + 1
        print count
        now = int(time.time())
