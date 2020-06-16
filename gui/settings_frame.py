from tkinter import *
from tkinter import ttk
import pandas as pd

class SettingsFrame:
    def __init__(self, parent, BG_COLOR, WIDGET_COLOR, s_api):
        self.BG_COLOR = BG_COLOR
        self.WIDGET_COLOR = WIDGET_COLOR

        self.frame = Frame(parent, bg=self.BG_COLOR[0])
        self.rows = 0

        #Shrimpy API settings
        Label(self.frame, text="Shrimpy API", bg=self.BG_COLOR[0], fg=self.WIDGET_COLOR[0], font="bold").grid(row=self.rows, column=0, sticky="w")
        self.rows += 1
        
        Label(self.frame, text="Public key", bg=self.BG_COLOR[0], fg=self.WIDGET_COLOR[0]).grid(row=self.rows, column=0, sticky="w")
        self.p_key_entry = Entry(self.frame, width=100)
        self.p_key_entry.grid(row=self.rows, column=1, columnspan=3); self.rows += 1

        Label(self.frame, text="Secret key", bg=self.BG_COLOR[0], fg=self.WIDGET_COLOR[0]).grid(row=self.rows, column=0, sticky="w")
        self.s_key_entry = Entry(self.frame, width=100, show="*")
        self.s_key_entry.grid(row=self.rows, column=1, columnspan=3); self.rows += 1
        
        Label(self.frame, text="Exchange*", bg=self.BG_COLOR[0], fg=self.WIDGET_COLOR[0]).grid(row=self.rows, column=0, sticky="w")
        self.exchange_cbox = ttk.Combobox(self.frame, textvariable=s_api.current_exchange, values=s_api.exchanges["exchange"].to_string(index=False))
        self.exchange_cbox.current(0)
        self.exchange_cbox.grid(row=self.rows, column=1, sticky="w")
        self.rows += 1
        
        self.separator(1)

        #Currency calculator settings 
        Label(self.frame, text="Currency calculator", bg=self.BG_COLOR[0], fg=self.WIDGET_COLOR[0], font="bold").grid(row=self.rows, column=0, sticky="w")
        self.rows += 1

        Label(self.frame, text="Default currency: from", bg=self.BG_COLOR[0], fg=self.WIDGET_COLOR[0]).grid(row=self.rows, column=0, sticky="w")
        self.cfrom_cbox = ttk.Combobox(self.frame, values=s_api.currency_strs)
        self.cfrom_cbox.grid(row=self.rows, column=1, sticky="w"); self.rows += 1 
        
        Label(self.frame, text="Default currency: to", bg=self.BG_COLOR[0], fg=self.WIDGET_COLOR[0]).grid(row=self.rows, column=0, sticky="w")
        self.cto_cbox = ttk.Combobox(self.frame, values=s_api.currency_strs)
        self.cto_cbox.grid(row=self.rows, column=1, sticky="w"); self.rows += 1 

        self.separator(2) 

        Label(self.frame, text="* = Requires a restart to take effect.", bg=self.BG_COLOR[0], fg=self.WIDGET_COLOR[0]).grid(row=self.rows, column=0, sticky="w")

    def separator(self, count):
        for i in range(count):
            Label(self.frame, text=" ", bg=self.BG_COLOR[0], fg=self.WIDGET_COLOR[0]).grid(row=self.rows, column=0, sticky="w")
            self.rows += 1