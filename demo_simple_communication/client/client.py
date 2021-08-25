import os
import time
import grpc
import logging
import random
random.seed(10)

from demo_pb2 import BrokerRequest
from demo_pb2_grpc import BrokerServiceStub
import config

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

class Client():
    """
    Client streams rows from a CSV file to the server and receives the response stream.
    """

    def __init__(self, port):
        channel = grpc.insecure_channel(port)
        self.stub = BrokerServiceStub(channel)
        self.simple_request(self.stub)
        

    def callback(self):
        """payload callback function"""
        request = BrokerRequest(id=int(random.randrange(1,999999)),
                                sensor1=float(random.uniform(0, 1)),
                                sensor2=float(random.uniform(0, 1)),
                                sensor3=float(random.uniform(0, 1)),
                                sensor4=float(random.uniform(0, 1)))
        return request

    def simple_request(self, stub):
        """The client streams data to the server and gets a single response back""" 
        response = stub.SimpleMethod(self.callback())
        logging.info("Server response payload: %d, %r", 
                    int(response.id), bool(response.prediction))


def main():
    Client(config.port)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted!")
        exit(0)