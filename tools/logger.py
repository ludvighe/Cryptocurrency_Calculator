import pandas as pd
import datetime as dt

class Logger:
    def __init__(self):
        self.calcs_log_path = "logs/calc_log_test.txt"
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_colwidth', None)
        pd.options.display.float_format = '{:20,.9f}'.format


    def log_calcs(self, data, labels):
        print(data)
        print(labels)
        now = dt.datetime.now()
        df = pd.DataFrame([data], index=["USD"], columns=labels)
        print(df)
        with open(self.calcs_log_path, "a+") as file:
            file.write(f"Logged: {dt.datetime.now()}\n{df}\n\n")
