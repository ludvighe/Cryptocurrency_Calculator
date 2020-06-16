from tkinter import *
from tkinter import ttk
import pandas as pd
import numpy as np
import traceback

class CurrencyCard:


    def __init__(self, parent, BG_COLOR, WIDGET_COLOR, index:int, s_api):
        self.parent = parent
        self.index = index 
        self.cdata = s_api.cdata 
        
        if (index % 2) == 0:
            bg = BG_COLOR[1]
        else:
            bg = BG_COLOR[0]

        self.frame = Frame(parent.frame, bg=bg)
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

        self.in_currency_cbox = ttk.Combobox(self.frame, values=s_api.currency_strs)
        self.in_currency_cbox.current(1)
        self.in_currency_cbox.grid(row=0, column=cols); cols += 1

        Label(self.frame, text="    ===>    ", bg=bg, fg=WIDGET_COLOR[0]).grid(row=0, column=cols)
        cols += 1

        self.out_entry = Entry(self.frame, textvariable="")
        self.out_entry.grid(row=0, column=cols); cols += 1

        self.out_currency_cbox = ttk.Combobox(self.frame, values=s_api.currency_strs)
        self.out_currency_cbox.current(0)
        self.out_currency_cbox.grid(row=0, column=cols); cols +=1
        
        self.calc_btn = Button(self.frame, text="Calculate", bg=WIDGET_COLOR[0], fg=WIDGET_COLOR[1], command=self.calculate)
        self.calc_btn.grid(row=0, column=cols); cols += 1
        
    def calculate(self):
        try:
            self.out_entry.delete(0, END)
            in_cdata = self.cdata.iloc[self.in_currency_cbox.current()].to_numpy()
            out_cdata = self.cdata.loc[self.out_currency_cbox.current()].to_numpy()
            in_usd = float(in_cdata[2])
            out_usd = float(out_cdata[2])
            self.exchange_rate = np.divide(in_usd, out_usd)
            self.result = np.multiply(float(self.in_entry.get()), self.exchange_rate)
            self.result_usd = np.multiply(self.result, out_usd)
            self.out_entry.insert(0, '{:.20f}'.format(self.result).rstrip("0"))
            #print(f"Calculated {in_cdata[2]} USD worth of {in_cdata[1]} to {out_cdata[2]} USD worth of {out_cdata[1]}\nWith exchange rate: {self.exchange_rate}%")
        except Exception as e:
            print(f"Could not calculate values for {self.in_label.get()}:\n{e}")
    
    def remove_ccard(self):
        self.parent.ccard_list.remove(self)
        self.frame.destroy()

    def get_calculated(self):
        self.calculate()
        return [self.result, self.result_usd, self.exchange_rate]

    def update_cdata(self, s_api):
        self.cdata = s_api.cdata

    def get_log_data(self):
        self.calculate()
        return [self.in_label.get(), self.result_usd]