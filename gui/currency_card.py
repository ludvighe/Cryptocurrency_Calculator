from tkinter import *
from tkinter import ttk
import pandas as pd
import numpy as np

class CurrencyCard:


    def __init__(self, parent, BG_COLOR, WIDGET_COLOR, index:int, cdata:pd.DataFrame):
        self.index = index 
        self.data = cdata 

        if (index % 2) == 0:
            bg = BG_COLOR[1]
        else:
            bg = BG_COLOR[0]

        self.frame = Frame(parent, bg=bg)
        cols = 0
        #self.in_label = Label(self.frame, text=f"Conversion {index}", bg=bg, fg=WIDGET_COLOR[0])
        #self.in_label.grid(row=0, column=0)
        
        Button(self.frame, text="-", fg=WIDGET_COLOR[0], command=self.remove_ccard).grid(row=0, column=cols, sticky="w")
        cols += 1
        Label(self.frame, text=" ", bg=bg).grid(row=0, column=cols)
        cols += 1

        self.in_label = Entry(self.frame, bg=bg, fg=WIDGET_COLOR[0])
        self.in_label.insert(0, f"Conversion {index}")
        self.in_label.grid(row=0, column=cols); cols += 1

        self.in_entry = Entry(self.frame)
        self.in_entry.grid(row=0, column=cols); cols += 1

        self.in_currency_cbox = ttk.Combobox(self.frame, values=self.data["symbol"].to_string(index=False))
        self.in_currency_cbox.grid(row=0, column=cols); cols += 1

        Label(self.frame, text="    ===>    ", bg=bg, fg=WIDGET_COLOR[0]).grid(row=0, column=cols)
        cols += 1

        self.out_entry = Entry(self.frame, textvariable="")
        self.out_entry.grid(row=0, column=cols); cols += 1

        self.out_currency_cbox = ttk.Combobox(self.frame, values=self.data["symbol"].to_string(index=False))
        self.out_currency_cbox.grid(row=0, column=cols); cols +=1
        
        self.calc_btn = Button(self.frame, text="Calculate", bg=WIDGET_COLOR[0], fg=WIDGET_COLOR[1], command=self.calculate)
        self.calc_btn.grid(row=0, column=cols); cols += 1
        
    def calculate(self):
        try:
            self.out_entry.delete(0, END)
            in_cdata = self.data.loc[self.data["symbol"] == self.in_currency_cbox.get()].to_numpy()
            out_cdata = self.data.loc[self.data["symbol"] == self.out_currency_cbox.get()].to_numpy()
            in_usd = in_cdata[0][2]
            out_usd = out_cdata[0][2]
            self.exchange_rate = float(in_usd) / float(out_usd)
            self.result = float(self.in_entry.get()) * self.exchange_rate
            self.result_usd = self.result * float(out_usd)
            self.out_entry.insert(0, self.result)
        except:
            #HANDLE THIS!
            pass
    
    def remove_ccard(self):
        self.frame.destroy()

    def get_calculated(self):
        self.calculate()
        return [self.result, self.result_usd, self.exchange_rate]

    def update_cdata(self, s_api):
        self.cdata = s_api.cdata