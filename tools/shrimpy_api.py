import shrimpy
import numpy as np
import pandas as pd
import json

class ShrimpyAPI:
    def __init__(self, public_key, secret_key):
        with open("settings.json") as f:
            self.settings = json.load(f)
        self.public_key = public_key
        self.secret_key = secret_key
        self.current_exchange = self.settings["default_exchange"]
        #np.set_printoptions(suppress=True, formatter={'float_kind':'{:8f}'.format})
        #pd.options.display.float_format = '{:20,.9f}'.format
        self.refresh()

    def refresh(self):
        #Get data from Shrimpy's API
        client = shrimpy.ShrimpyApiClient(self.public_key, self.secret_key)
        self.cdata = pd.DataFrame(client.get_ticker(self.current_exchange))
        self.exchanges = pd.DataFrame(client.get_supported_exchanges())

        #Currency strings for comboboxes
        self.currency_strs = list()

        appendices = list()

        for i in range(len(self.cdata)):
            name = self.cdata["name"][i]
            symbol = self.cdata["symbol"][i]
            self.currency_strs.append(f"{name} ({symbol})")

            #Other support
            hundred_millionth = 0.00000001
            if symbol in ["BTC", "ETH", "LTC"]:
                hmil_usd = np.multiply(float(self.cdata["priceUsd"][i]), hundred_millionth)
                hmil_btc = np.multiply(float(self.cdata["priceBtc"][i]), hundred_millionth)
                pchange = self.cdata["percentChange24hUsd"][i]
                updated = self.cdata["lastUpdated"][i]
                
                if symbol == "BTC":
                    appendices.append(pd.DataFrame([["Satoshi", "Satoshi", hmil_usd, hmil_btc, pchange, updated]], columns=self.cdata.columns))
                elif symbol == "ETH":
                    appendices.append(pd.DataFrame([["Gwei", "Gwei", hmil_usd, hmil_btc, pchange, updated]], columns=self.cdata.columns))
                elif symbol == "LTC":
                    appendices.append(pd.DataFrame([["Litoshi", "Litoshi", hmil_usd, hmil_btc, pchange, updated]], columns=self.cdata.columns))
        
        for df in appendices:
            self.cdata = self.cdata.append(df, ignore_index=True)
            name = df["name"][0]
            symbol = df["symbol"][0]
            self.currency_strs.append(f"{name} ({symbol})")

    def currency_str_index(self, s):
        for i in range(len(self.currency_strs)):
            if s in self.currency_strs[i]: 
                print(f"Found: {self.currency_strs[i]}")
                return i