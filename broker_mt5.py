 # Broker integration with MetaTrader 5
from MetaTrader5 import MetaTrader5
class BrokerMT5:
    def __init__(self):
        self.mt5 = MetaTrader5()
        
    def connect(self):
        self.mt5.initialize()
        
    def disconnect(self):
        self.mt5.shutdown()
