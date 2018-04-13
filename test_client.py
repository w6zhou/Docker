import grpc

import helloword_pb2, helloword_pb2_grpc


def box_unlock():
    channel = grpc.insecure_channel("%s:%d" % ('10.233.65.95', '54321'))
    stub = helloword_pb2_grpc.GreeterStub(channel)
    kwargs = {'name': 'wenqi', 'name2': 'wenqi2'}
    req = helloword_pb2.HelloRequest(**kwargs)
    response = stub.SayHello(req, 30)
    print response
    return response


if __name__ == "__main__":
    box_unlock()
