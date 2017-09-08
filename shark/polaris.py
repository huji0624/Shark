#!/usr/bin/python


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

'''
the data collect module for the shark.
'''
class Polaris:
    def __init__(self):
        self.record = {}

    def mark_chips_change(self,name,chips,round_count):
        if "chips" not in self.record:
            self.record["chips"] = {}
        chips_record = self.record["chips"]
        if round_count not in chips_record:
            chips_record[round_count] = []
        chips_record[round_count].append((name,chips))

    def show(self,save_path=None):
        chips_record = self.record["chips"]
        round_counts = sorted(chips_record.keys())
        datas = []
        col = []
        for round_count in round_counts:
            status = chips_record[round_count]
            status = sorted(status,key=lambda tmp : tmp[0])
            round_data = []
            for s in status:
                if len(col) < len(status):
                    col.append(s[0])
                round_data.append(s[1])
            datas.append(round_data)
        df = pd.DataFrame(datas, index=round_counts, columns=col)
        ax = df.plot()
        if save_path:
            ax.get_figure().savefig(save_path)
        else:
            plt.show()