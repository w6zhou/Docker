import time

import grpc
from concurrent import futures

import helloword_pb2, helloword_pb2_grpc


def test_server(request):
    return {'message': 'hellow'}


class Greeter(helloword_pb2_grpc.GreeterServicer):
    def SayHello(self, request, context):
        print 'hellow'
        return helloword_pb2.HelloReply(**test_server(request))


def start_server():

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    helloword_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port('%s:%s' % ('10.233.65.95', '54321'))
    server.start()

    try:
        while True:
            time.sleep(24 * 60 * 60)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    start_server()