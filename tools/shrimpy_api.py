import shrimpy
import numpy as np
import pandas as pd

class ShrimpyAPI:
    def __init__(self, public_key, secret_key):
        self.public_key = public_key
        self.secret_key = secret_key
        self.current_exchange = "binance"
        self.refresh()

    #Get data from Shrimpy's API
    def refresh(self):
        client = shrimpy.ShrimpyApiClient(self.public_key, self.secret_key)
        self.cdata = pd.DataFrame(client.get_ticker(self.current_exchange))
        self.exchanges = pd.DataFrame(client.get_supported_exchanges())
    

