#!/usr/bin/python


from Tkinter import *


class HandsReplayer():
    def __init__(self, master):
        self.frame = Frame(master, bg="gray", width=800, height=400)
        self.frame.grid(row=0, column=1)
        self.subviews = None

    def clear(self):
        if self.subviews:
            for view in self.subviews:
                view.place_forget()
        self.subviews = []

    def place_players(self, record):
        players = record['players']
        x = self.frame.winfo_width() / 5
        y = self.frame.winfo_height() / 4
        count = 0
        for player in players:
            count = count + 1
            label = Label(self.frame, text="%s[%s]" % (player["name"], player["chips"]))
            label.place(x=x, y=y)
            self.subviews.append(player)
            x = x + 200
            if count >= len(players) / 2:
                count = 0
                y = self.frame.winfo_height() / 4 * 3
                x = self.frame.winfo_width() / 5

    def play_action(self):
        pass

    def place_play_button(self):
        play_bt = Button(self.frame, text="Play", command=self.play_action)
        play_bt.place(x=self.frame.winfo_width() / 20, y=self.frame.winfo_height() / 20)
        self.subviews.append(play_bt)

    def play(self, record):
        self.clear()
        self.place_play_button()
        self.place_players(record)
        print record
