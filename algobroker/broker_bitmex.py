#!/usr/bin/python3
# Copyright (C) 2015 Bitquant Research Laboratories (Asia) Limited
# Released under the Simplified BSD License

import my_path
import pprint
import algobroker
from algobroker import Broker
from cryptoexchange import bitmex

class BrokerBitmex(Broker):
    def __init__(self):
        Broker.__init__(self, "broker_bitmex")
        self.api = None
    def process_data(self, data):
        if self.api == None:
            self.error("keys not initialized")
            self.error(pprint.pformat(data))
            return
        cmd = data.get('cmd', None)
        if cmd == 'order':
            self.api.place_order(data.get('quantity', None),
                                 data.get('symbol', None),
                                 data.get('price', None))
        elif cmd == 'cancel':
            self.api.cancel(data.get('orderID', None))
        elif cmd == 'cancel_all':
            orders = self.api()
            for i in orders:
                self.api.cancel(i)
    def process_control(self, data):
        self.info("received control message")
        try:
            if data.get('cmd', None) == "auth":
                base_url = data.get('base_url', None)
                login = data.get('login', None)
                password = data.get('password', None)
                otpToken = data.get('otpToken', None)
                apiKey = data.get('apiKey', None)
                apiSecret = data.get('apiSecret', None)
                orderIDPrefix = data.get('orderIDPrefix', 'broker_bitmex_')
                self.api = bitmex.BitMEX(base_url,
                                         login,
                                         password,
                                         otpToken,
                                         apiKey,
                                         apiSecret,
                                         orderIDPrefix)
        except:
            self.error("error processing control message")

if __name__ == "__main__":
    bp = BrokerBitmex()
    bp.run()