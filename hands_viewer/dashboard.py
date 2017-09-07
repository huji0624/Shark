#!/usr/bin/python

from Tkinter import *
from FileDialog import *
from hands_replayer import *


class DashBoard:
    def __init__(self, master):
        self.master = master
        self.board = None
        self.hands_list = None
        self.replayer = None
        self.record = None

    def clear(self):
        self.hands_list.delete(0, self.hands_list.size())

    def choose_file(self,file_path):
        print file_path
        import json
        self.clear()
        f = file(file_path, "r")
        text = f.read()
        print text
        self.record = json.loads(text)
        f.close()
        for item in self.record:
            self.hands_list.insert(0, item['name'])

    def choose_file_handler(self):
        fd = LoadFileDialog(self.master)
        file_path = fd.go()
        self.choose_file(file_path)

    def choose_hand(self,event):
        location = self.hands_list.curselection()[0]
        import copy
        record_ = copy.deepcopy(self.record[location])
        self.replayer.play(record_)

    def show(self):
        self.board = Frame(self.master)
        self.board.grid(row=0,column=0)
        self.hands_list = Listbox(self.board,height=20)
        self.hands_list.bind('<<ListboxSelect>>', self.choose_hand)
        self.hands_list.pack()
        choos_file_bt = Button(self.board, text="ChooseHand", command=self.choose_file_handler)
        choos_file_bt.pack()
        self.replayer = HandsReplayer(self.master)
        self.choose_file("/Users/huji/Documents/learn/Shark/hands_viewer/test.json")

