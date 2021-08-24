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
        self.bidirectional_streaming(self.stub)
        

    def stream_messages(self):
        """Server request callback function"""
        index = 0
        while(True):
            index = index+1
            request = BrokerRequest(id=int(index),
                                    sensor1=float(random.uniform(0, 1)),
                                    sensor2=float(random.uniform(0, 1)),
                                    sensor3=float(random.uniform(0, 1)),
                                    sensor4=float(random.uniform(0, 1)))
            yield request
            time.sleep(config.streaming_rate)

    def bidirectional_streaming(self, stub):
        response_iterator = stub.BidirectionalStreaming(self.stream_messages())
        for response in response_iterator:
            logging.info("Server response: %d, %r", int(response.id),
                  bool(response.prediction))


def main():
    Client(config.port)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted!")
        exit(0)