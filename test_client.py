import time

import grpc

import helloword_pb2, helloword_pb2_grpc


def box_unlock():
    channel = grpc.insecure_channel("%s:%s" % ('www.goserver.com', '80'))
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
    # from hyper import HTTPConnection
    #
    # # conn = HTTP20Connection('nghttp2.org:443')
    # # conn.request('GET', '/httpbin/get')
    # conn = HTTPConnection('php.svc.mfw')
    # conn.secure = False
    # conn.request('GET', '/?name=caodi&name2=haha')
    # resp = conn.get_response()
    #
    # print(resp.read())
