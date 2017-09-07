#!/usr/bin/python


import log


class HandsRecorder:
    def __init__(self,save_path):
        self.save_path = save_path
        self.hands = []

    def save_to_file(self):
        if self.save_path is None:
            log.logW("save path not set.")
            return
        import json
        str = json.dumps(self.hands)
        print self.save_path
        f = file(self.save_path,"w")
        f.write(str)
        f.close()

    def new_hand(self,name):
        if self.save_path is None:
            return
        self.cur_hand = {}
        self.cur_hand["name"] = name
        self.cur_hand["players"]=[]
        self.cur_hand["board"]=[]
        self.cur_hand["preflop"]=[]
        self.cur_hand["flop"]=[]
        self.cur_hand["turn"]=[]
        self.cur_hand["river"]=[]
        self.cur_hand["pots"]=[]
        self.cur_hand["result"]={}

    def add_pot(self,pot):
        if self.save_path is None:
            return
        self.cur_hand["pots"].append(pot)

    def add_player(self,name,chips,hand_cards):
        if self.save_path is None:
            return
        self.cur_hand["players"].append({"name":name,"chips":chips,"hand_cards":hand_cards})

    def add_board_card(self,card):
        if self.save_path is None:
            return
        self.cur_hand["board"].append(card)

    def add_pre_flop_action(self,name,action_type,to_chips):
        if self.save_path is None:
            return
        self.cur_hand["preflop"].append((name,action_type,to_chips))

    def add_flop_action(self,name,action_type,to_chips):
        if self.save_path is None:
            return
        self.cur_hand["flop"].append((name, action_type, to_chips))

    def add_turn_action(self,name,action_type,to_chips):
        if self.save_path is None:
            return
        self.cur_hand["turn"].append((name, action_type, to_chips))

    def add_river_action(self,name,action_type,to_chips):
        if self.save_path is None:
            return
        self.cur_hand["river"].append((name, action_type, to_chips))

    def end_hand(self,result):
        if self.save_path is None:
            return
        self.cur_hand["result"] = result
        self.hands.append(self.cur_hand)
        self.cur_hand = None