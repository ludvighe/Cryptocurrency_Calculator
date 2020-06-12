import tkinter
from tkinter import *
from tkinter import ttk
import numpy as np
import pandas as pd
from gui import currency_card
from tools import logger


class CalcFrame:


    def __init__(self, parent, BG_COLOR, WIDGET_COLOR, s_api):
        self.BG_COLOR = BG_COLOR
        self.WIDGET_COLOR = WIDGET_COLOR
        self.cdata = s_api.cdata
        self.lgr = logger.Logger()

        self.frame = Frame(parent, bg=self.BG_COLOR[0])

        self.rows = 0
        self.ccard_list = list()
        self.add_ccard()

        Button(self.frame, text="+", fg=WIDGET_COLOR[0], command=self.add_ccard).grid(row=100, column=0, sticky="w")

        #Sub frame
        sub_frame = Frame(self.frame, bg=WIDGET_COLOR[0])
        sub_frame.place(relwidth=1, relheight=0.1, relx=0, rely=0.9)

        self.total_cbox = ttk.Combobox(sub_frame, values=self.cdata["symbol"].to_string(index=False))
        self.total_cbox.place(relwidth=0.15, relheight=0.5, relx=0.05, rely=0.25)
        self.total_entry = Entry(sub_frame)
        self.total_entry.place(relwidth=0.5, relheight=0.5, relx=0.25, rely=0.25)
        Button(sub_frame, bg=WIDGET_COLOR[0], fg=WIDGET_COLOR[1], text="Calculate total", command=self.calc_total).place(relwidth=0.1, relheight=1, relx=0.8, rely=0)
        Button(sub_frame, bg=WIDGET_COLOR[0], fg=WIDGET_COLOR[1], text="Log", command=self.log).place(relwidth=0.1, relheight=1, relx=0.9, rely=0)

    def add_ccard(self):
        if len(self.ccard_list) <= 0:
            c = currency_card.CurrencyCard(self, self.BG_COLOR, self.WIDGET_COLOR, len(self.ccard_list), self.cdata)
        else:
            c = currency_card.CurrencyCard(self, self.BG_COLOR, self.WIDGET_COLOR, (self.ccard_list[len(self.ccard_list) - 1].index + 1), self.cdata)
        self.ccard_list.append(c)
        c.frame.grid(row=self.rows, column=0)
        self.rows += 1
    

    def calc_total(self):
        total = 0
        try:
            for i in self.ccard_list:
                total += i.get_calculated()[1]
             
            self.total_entry.delete(0, END)
            in_cdata = self.cdata.loc[self.cdata["symbol"] == "BTC"].to_numpy()
            out_cdata = self.cdata.loc[self.cdata["symbol"] == self.total_cbox.get()].to_numpy()
            in_usd = in_cdata[0][3]
            out_usd = out_cdata[0][2]
            self.exchange_rate = float(in_usd) / float(out_usd)
            self.result = float(total) * self.exchange_rate
            self.total_entry.insert(0, self.result)
        
        except:
            #HANDLE THIS!!
            pass

    def refresh_cdata(self, s_api):
        self.cdata = s_api.cdata
        for i in self.ccard_list:
            i.update_cdata(s_api)

    def log(self):
        data = list()
        labels = list()

        for i in self.ccard_list:
            res = i.get_log_data()
            labels.append(res[0])
            data.append(res[1])

        self.lgr.log_calcs(data, labels)
