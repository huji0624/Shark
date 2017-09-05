#!/usr/bin/python

from Tkinter import *

def show(master):
    board = Frame(master)
    board.pack()
    hands_list = Listbox(board)
    for i in range(0,30):
        hands_list.insert(0,i)