
import tkinter
from tkinter import *
import pandas as pd
import sys
from gui import calc_frame, settings_frame, key_frame
from tools import shrimpy_api, saves, logger

class Main:
    def __init__(self):

        #BG_COLOR= ["#808090", "#9999A6"] #Dark to light
        self.BG_COLOR= ["#F4F4F4", "#DBDBDB"] #Dark to light
        #WIDGET_COLOR = ["#6E2594", "#EEE0CB"] #[0]=Background, [1]=Foreground
        self.WIDGET_COLOR = ["#0375B4", "#FFFFFF"] #[0]=Background, [1]=Foreground
        self.rows = cols = 0

        #ROOT SETUP
        self.root = Tk()
        self.root.geometry("850x600")
        self.root.minsize(550, 250)
        self.root.title("Cryptocurrency Calculator")

        #Intro screen
        self.key_enetered = False
        self.kframe = key_frame.KeyFrame(self.root, self.BG_COLOR, self.WIDGET_COLOR) 
        Button(self.kframe.frame, text="Done", bg=self.WIDGET_COLOR[0], fg=self.WIDGET_COLOR[1], command=self.frame_inits).grid(row=100, column=0, sticky="w")
        self.kframe.frame.place(relwidth=1, relheight=1, relx=0, rely=0)

        def keyListener(event):
            self.root.quit()

        #BINDS
        #root.bind('q', keyListener)

        self.root.mainloop()

    def frame_inits(self):
        try:
            #Init cryptocurrency market data from Shirimpy's API
            self.s_api = shrimpy_api.ShrimpyAPI(self.kframe.p_key_entry.get(), self.kframe.s_key_entry.get())
            self.key_enetered = True
        except Exception as e:
            print(f"Could not get data from Shrimpy:\n{e}")
        
        if self.key_enetered:

            #BUILD MAIN FRAME
            self.mf_relwidth = 1
            self.mf_relheight = 0.05
            self.mainFrame = Frame(self.root, bg=self.WIDGET_COLOR[0])
            self.mainFrame.place(relwidth=self.mf_relwidth, relheight=self.mf_relheight, relx=0, rely=0)
            

            self.cframe = calc_frame.CalcFrame(self.root, self.BG_COLOR, self.WIDGET_COLOR, self.s_api)
            self.sframe = settings_frame.SettingsFrame(self.root, self.BG_COLOR, self.WIDGET_COLOR, self.s_api)


            #BUILD WIDGETS
            top_calc_btn = Button(self.mainFrame, bg=self.WIDGET_COLOR[0], fg=self.WIDGET_COLOR[1], text="Currency calculator", command=self.show_calc_frame)
            top_calc_btn.place(relwidth=0.2, relheight=1, relx=0, rely=0)
            top_sett_btn = Button(self.mainFrame, bg=self.WIDGET_COLOR[0], fg=self.WIDGET_COLOR[1], text="Settings", command=self.show_settings_frame)
            top_sett_btn.place(relwidth=0.2, relheight=1, relx=0.2, rely=0)
            top_refresh_btn = Button(self.mainFrame, bg=self.WIDGET_COLOR[0], fg=self.WIDGET_COLOR[1], text="Refresh market data", command=self.refresh_cdata)
            top_refresh_btn.place(relwidth=0.2, relheight=1, relx=0.8, rely=0)

            self.show_calc_frame()




    def show_calc_frame(self):
        if self.key_enetered:
            self.kframe.frame.place_forget()
            self.sframe.frame.place_forget()

            self.cframe.frame.place(relwidth=1, relheight=(1-self.mf_relheight), relx=0, rely=self.mf_relheight)

    def show_settings_frame(self):
        if self.key_enetered:
            self.kframe.frame.place_forget()
            self.sframe.frame.place_forget()
            
            self.sframe.frame.place(relwidth=1, relheight=(1-self.mf_relheight), relx=0, rely=self.mf_relheight)

    def refresh_cdata(self):
        try:
            self.s_api.refresh()
            self.cframe.refresh_cdata(self.s_api)
        except Exception as e:
            print(f"Coult not refresh market data:\n{e}")
            


