import os
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
from signal import signal, SIGTERM
import grpc
from grpc_interceptor import ExceptionToStatusInterceptor
from grpc_interceptor.exceptions import NotFound
import logging
import math

from demo_pb2 import BrokerResponse
import demo_pb2_grpc
import config

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

class BrokerServiceServicer(demo_pb2_grpc.BrokerServiceServicer):

    def BidirectionalStreaming(self, request_iterator, context):
        """Server request callback function"""
        if not request_iterator:
            raise NotFound("Client request is incorrect!")

        for request in request_iterator:
            logging.info("Client request: %d %g %g %g %g",
                  request.id,
                  request.sensor1,
                  request.sensor2,
                  request.sensor3,
                  request.sensor4)

            if (self.isPrimeNumber(request.id) == True):
                yield BrokerResponse(id=request.id, prediction=True)
            else:
                yield BrokerResponse(id=request.id, prediction=False)

    def isFibonacci(self, n):
        return self.isPerfectSquare(5*n*n + 4) or self.isPerfectSquare(5*n*n - 4)

    def isPerfectSquare(self, x):
        s = int(math.sqrt(x))
        return s*s == x

    def isPrimeNumber(self, num):
        flag = True
        if num > 1:
            for i in range(2, num):
                if (num % i) == 0:
                    flag = False
                    break
        return flag
        

def main():
    interceptors = [ExceptionToStatusInterceptor()]
    server = grpc.server(
        ThreadPoolExecutor(max_workers=10),
        interceptors=interceptors)
    demo_pb2_grpc.add_BrokerServiceServicer_to_server(
        BrokerServiceServicer(),
        server)
    server.add_insecure_port(config.port)

    logging.info("Starting server. Listening on port : %s", str(config.port))
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted!")
        exit(0)