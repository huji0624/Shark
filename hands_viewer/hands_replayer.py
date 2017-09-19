#!/usr/bin/python


from Tkinter import *
from deuces import *
import math


class HandsReplayer():
    def __init__(self, master):
        self.frame = Frame(master, bg="gray", width=600, height=600)
        self.frame.grid(row=0, column=1)
        self.subviews = None
        self.end_label = None
        self.pot_label = None
        self.board_label = None
        self.action_labels = None

    def clear(self):
        if self.action_labels:
            self.clear_views(self.action_labels)
        if self.subviews:
            self.clear_views(self.subviews)
        if self.pot_label:
            self.pot_label.place_forget()
            self.pot_label = None
        if self.board_label:
            self.board_label.place_forget()
            self.board_label = None
        if self.end_label:
            self.end_label.place_forget()
            self.end_label = None

    def init_player(self,record):
        self.record = record
        self.subviews = []
        self.player_labels = {}
        self.action_labels = []
        self.board_label = Label(self.frame, text="")
        cx, cy = self.center()
        self.board_label.place(x=cx, y=cy)
        self.pot_label = Label(self.frame,text="")
        self.pot_label.place(x=cx,y=cy-50)
        self.end_label = None

    def center(self):
        return self.frame.winfo_width()/2,self.frame.winfo_height()/2

    def position_with_degree(self,degree):
        R = 250
        cx, cy = self.center()
        x = cx + R * math.cos(degree)
        y = cy + R * math.sin(degree)
        return x,y

    def place_players(self, record):
        players = record['players']
        degree = 0
        dd = math.pi*2 / len(players)
        for player in players:
            x,y = self.position_with_degree(degree)
            label = Label(self.frame, text="%s[%s]\n[%s]" % (player["name"], player["chips"],self.cards_to_str(player["hand_cards"])))
            label.place(x=x, y=y)
            self.player_labels[player["name"]] = label
            self.subviews.append(label)
            degree = degree + dd

    def cards_to_str(self,hands):
        s = ""
        for card in hands:
            s = s + Card.int_to_str(card) + " "
        return s

    def clear_views(self,views):
        if views:
            for view in views:
                view.place_forget()

    def play_action(self):
        if self.end_label:
            return

        if len(self.record["preflop"]) > 0:
            self.excute_action(self.record["preflop"].pop(0))
            return
        pots = self.record["pots"]
        board = self.record["board"]
        if len(board) >=3:
            self.clear_views(self.action_labels)
            self.draw_pot(pots)
            self.draw_card(board.pop(0))
            self.draw_card(board.pop(0))
            self.draw_card(board.pop(0))
            return
        if len(self.record["flop"]) > 0:
            self.excute_action(self.record["flop"].pop(0))
            return
        if len(board) >=2:
            self.clear_views(self.action_labels)
            self.draw_pot(pots)
            self.draw_card(board.pop(0))
            return
        if len(self.record["turn"]) > 0:
            self.excute_action(self.record["turn"].pop(0))
            return
        if len(board) >=1:
            self.clear_views(self.action_labels)
            self.draw_pot(pots)
            self.draw_card(board.pop(0))
            return
        if len(self.record["river"]) > 0:
            self.excute_action(self.record["river"].pop(0))
            return
        if len(pots) == 1:
            self.draw_pot(pots)
            return
        self.end(self.record["result"])

    def draw_pot(self,pots):
        if len(pots) > 0:
            self.pot_label["text"] = pots.pop(0)

    def draw_card(self,card):
        self.board_label["text"] = self.board_label["text"] + Card.int_to_str(card) + " "

    def excute_action(self,action):
        name = action[0]
        action_type = action[1]
        chips = action[2] if len(action) == 3 else 0
        label = self.player_labels[name]
        cx , cy = self.center()
        lx = (cx + label.winfo_x())/2
        ly = (cy + label.winfo_y())/2
        action_label = Label(self.frame, text="%s[%s]" % (action_type,chips))
        action_label.place(x=lx,y=ly)
        self.action_labels.append(action_label)

    def end(self,result):
        self.clear_views(self.action_labels)
        for k,v in result.items():
            if v>0:
                self.excute_action((k,"win",v))
            elif v<0:
                self.excute_action((k, "lose", v))
        self.end_label = Label(self.frame,text="END",bg="red")
        cx, cy = self.center()
        self.end_label.place(x=cx,y=cy+50)

    def place_play_button(self):
        play_bt = Button(self.frame, text="Play", command=self.play_action)
        play_bt.place(x=self.frame.winfo_width() / 20, y=self.frame.winfo_height() / 20)
        self.subviews.append(play_bt)

    def play(self, record):
        self.clear()
        self.init_player(record)
        self.place_play_button()
        self.place_players(record)
