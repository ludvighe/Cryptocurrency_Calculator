import tkinter
from tkinter import *
from tkinter import ttk
import numpy as np
import pandas as pd
from gui import currency_card
from tools import logger
import traceback
import json


class CalcFrame:


    def __init__(self, parent, BG_COLOR, WIDGET_COLOR, s_api):
        self.BG_COLOR = BG_COLOR
        self.WIDGET_COLOR = WIDGET_COLOR
        self.s_api = s_api
        self.cdata = s_api.cdata
        self.lgr = logger.Logger()
        
        self.frame = Frame(parent, bg=self.BG_COLOR[0])

        # Load Settings
        with open("settings.json") as f:
            global settings
            settings = json.load(f)

        self.rows = 0
        self.ccard_list = list()

        if len(settings["initial_pairs"]) > 0:
            for pair in settings['initial_pairs']:
                print(pair)
                self.add_ccard(symbol_from=pair[0], symbol_to=pair[1])
        else:
            self.add_ccard()

        Button(self.frame, text="+", fg=WIDGET_COLOR[0], command=self.add_ccard).grid(row=100, column=0, sticky="w")

        #Sub frame
        sub_frame = Frame(self.frame, bg=WIDGET_COLOR[0])
        sub_frame.place(relwidth=1, relheight=0.1, relx=0, rely=0.9)

        self.total_cbox = ttk.Combobox(sub_frame, values=self.s_api.currency_strs)
        self.total_cbox.current(s_api.currency_str_index(settings["initial_total_token"]))
        self.total_cbox.place(relwidth=0.15, relheight=0.5, relx=0.05, rely=0.25)
        self.total_entry = Entry(sub_frame)
        self.total_entry.place(relwidth=0.5, relheight=0.5, relx=0.25, rely=0.25)
        Button(sub_frame, bg=WIDGET_COLOR[0], fg=WIDGET_COLOR[1], text="Calculate total", command=self.calc_total).place(relwidth=0.1, relheight=1, relx=0.8, rely=0)
        Button(sub_frame, bg=WIDGET_COLOR[0], fg=WIDGET_COLOR[1], text="Log", command=self.log).place(relwidth=0.1, relheight=1, relx=0.9, rely=0)

    def add_ccard(self, symbol_from="", symbol_to=""):
        if len(self.ccard_list) <= 0:
            c = currency_card.CurrencyCard(self, self.BG_COLOR, self.WIDGET_COLOR, len(self.ccard_list), self.s_api, symbol_from=symbol_from, symbol_to=symbol_to)
        else:
            c = currency_card.CurrencyCard(self, self.BG_COLOR, self.WIDGET_COLOR, (self.ccard_list[len(self.ccard_list) - 1].index + 1), self.s_api, symbol_from=symbol_from, symbol_to=symbol_to)
        self.ccard_list.append(c)
        c.frame.grid(row=self.rows, column=0)
        self.rows += 1
    

    def calc_total(self):
        self.total_usd = 0
        try:
            for i in self.ccard_list:
                self.total_usd += i.get_calculated()[1]
             
            self.total_entry.delete(0, END)
            in_cdata = self.cdata.loc[self.cdata["symbol"] == "BTC"].to_numpy()
            out_cdata = self.cdata.iloc[self.total_cbox.current()].to_numpy()
            in_usd = in_cdata[0][3]
            out_usd = out_cdata[2]
            self.exchange_rate = np.divide(float(in_usd), float(out_usd))
            self.result = np.multiply(float(self.total_usd), self.exchange_rate)
            self.total_entry.insert(0, '{:.20f}'.format(self.result).rstrip("0"))
        
        except Exception as e:
            print(in_cdata)
            print(out_cdata)
            print(f"Could not calculate total:\n{e}")

    def refresh_cdata(self, s_api):
        self.cdata = s_api.cdata
        for i in self.ccard_list:
            i.update_cdata(s_api)

    def log(self):
        self.calc_total()

        data = list()
        labels = list()
        #total = 0

        for i in self.ccard_list:
            res = i.get_log_data()
            labels.append(res[0])
            data.append(res[1])
            #total += res[1]

        data.append(self.total_usd)
        labels.append("Total") 

        self.lgr.log_calcs(data, labels)
