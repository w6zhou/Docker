import time

import grpc
from concurrent import futures

import helloword_pb2, helloword_pb2_grpc


def test_server(request):
    return {'message': 'hellow'}


class RpcTransaction(helloword_pb2_grpc.RpcTransactionServicer):
    def SayHello(self, request, context):
        return helloword_pb2.HelloReply(**test_server(request))


def start_server():

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    helloword_pb2_grpc.add_RpcTransactionServicer_to_server(RpcTransaction(), server)
    server.add_insecure_port('%s:%s' % ('localhost', ''))
    server.start()

    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    start_server()