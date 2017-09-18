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

    def plot_all(self,save_path=None):
        chips_record = self.record["chips"]
        round_counts = sorted(chips_record.keys())
        datas = []
        col = []
        av_datas = []
        av_round_counts = []
        for round_count in round_counts:
            status = chips_record[round_count]
            status = sorted(status,key=lambda tmp : tmp[0])
            round_data = []
            av_round_data = None
            if round_count % 100 == 0:
                av_round_data = []
                av_round_counts.append(round_count)
            for s in status:
                if len(col) < len(status):
                    col.append(s[0])
                round_data.append(s[1])
                if av_round_data is not None:
                    av_round_data.append(s[1]*100/round_count)
            datas.append(round_data)
            if av_round_data is not None:
                av_datas.append(av_round_data)
        df = pd.DataFrame(datas, index=round_counts, columns=col)
        av_df = pd.DataFrame(av_datas, index=av_round_counts, columns=col)
        ax = df.plot()
        av_ax = av_df.plot()
        ax.set_ylabel("chips gain")
        av_ax.set_ylabel("chips gain/100hands")
        if save_path:
            ax.get_figure().savefig(save_path)
            import os
            bn = os.path.basename(save_path)
            av_file_name = "av_" + bn
            av_ax.get_figure().savefig(save_path.replace(bn,av_file_name))
        else:
            plt.show()