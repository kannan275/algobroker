#!/usr/bin/python3
# Copyright (C) 2015 Bitquant Research Laboratories (Asia) Limited
# Released under the Simplified BSD License

import my_path
import time
import zmq
import algobroker
from algobroker import AlgoObject
import msgpack
import pprint
from yahoo_finance import Share

class YahooTicker(AlgoObject):
    def __init__(self):
        AlgoObject.__init__(self, "ticker_yahoo", zmq.PUB)
        self._data_socket.bind(algobroker.data_ports["ticker_yahoo"])
        self.time_limits = {}
        self.state = {}
        self.prev_state = {}
        self.assets = []
        self.quotes = {}
        self.timeout = 30000
        self.sleep = 30
        self.maintainence = 60 * 30
    def get_quotes(self):
        self.debug("getting quotes")
        try:
            for i in self.assets:
                yahoo = Share(i)
                self.quotes[i] = {
                    "source" : "yahoo",
                    "last" : float(yahoo.get_price())
                    }
        except OSError:
            self.error("Network Error")
    def send_quotes(self):
        self.debug("Sending quotes")
        self.send_data(self.quotes)
    def test(self):
        self.get_quotes()
        socket = self._context.socket(zmq.PUSH)
        socket.bind(algobroker.ports.dispatcher)
        message = { 'action' : 'log',
                    'item' : self.quotes }
        self._logger.debug("Sending data")
        socket.send(msgpack.packb(message))
    def process_control(self, data):
        self.debug("received control message")
        if data['cmd'] == "set":
            if 'assets' in data:
                self.debug("setting asset list")
                self.debug(pprint.pformat(data['assets']))
                self.assets = data['assets']
    def run_once(self):
        self.debug("running loop function")
        self.get_quotes()
        self.send_quotes()

if __name__ == "__main__":
    yq = YahooTicker()
    yq.run()