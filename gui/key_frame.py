from tkinter import *

class KeyFrame:
    def __init__(self, parent, BG_COLOR, WIDGET_COLOR):
        self.frame = Frame(parent, bg=BG_COLOR[0])
        rows = 0
        s = "This app uses Shrimpy's API to get market data.\nPlease enter you public key and secret key to use Cryptocurrency Calculator.\nLeave fields below empty for generic calls."
        Label(self.frame, text=s, bg=BG_COLOR[0], fg=WIDGET_COLOR[0]).grid(row=rows, column=0, columnspan=2)#, sticky="w")
        rows += 1
        
        Label(self.frame, text="Public key", bg=BG_COLOR[0], fg=WIDGET_COLOR[0]).grid(row=rows, column=0, sticky="w")
        self.p_key_entry = Entry(self.frame, width=100)
        self.p_key_entry.grid(row=rows, column=1); rows += 1

        Label(self.frame, text="Secret key", bg=BG_COLOR[0], fg=WIDGET_COLOR[0]).grid(row=rows, column=0, sticky="w")
        self.s_key_entry = Entry(self.frame, width=100, show="*")
        self.s_key_entry.grid(row=rows, column=1); rows += 1

