import grpc

import helloword_pb2, helloword_pb2_grpc


def box_unlock():
    channel = grpc.insecure_channel("%s:%d" % ('localhost', ''))
    stub = helloword_pb2_grpc.RpcBoxStub(channel)
    kwargs = {'name': 'wenqi', 'name2': 'wenqi2'}
    req = helloword_pb2.BoxUnlockReq(**kwargs)
    response = stub.BoxUnlock(req, 30)
    print response
    return response


if __name__ == "__main__":
    box_unlock()
