#!/usr/bin/python


import log
import round_state


class HandsRecorder:
    def __init__(self):
        self.hands = []

    def set_save_path(self,path_):
        self.save_path = path_

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
        self.hands = []

    def new_hand(self,name):
        self.cur_hand = {}
        self.cur_hand["name"] = name
        self.cur_hand["players"]=[]
        self.cur_hand["board"]=[]
        self.cur_hand[round_state.ROUND_STATE_PRE]=[]
        self.cur_hand[round_state.ROUND_STATE_FLOP]=[]
        self.cur_hand[round_state.ROUND_STATE_TURN]=[]
        self.cur_hand[round_state.ROUND_STATE_RIVER]=[]
        self.cur_hand["pots"]=[]
        self.cur_hand["result"]={}

    def add_pot(self,pot):
        self.cur_hand["pots"].append(pot)

    def add_player(self,name,chips,hand_cards):
        self.cur_hand["players"].append({"name":name,"chips":chips,"hand_cards":hand_cards})

    def add_board_card(self,card):
        self.cur_hand["board"].append(card)

    def add_round_action(self,round_name,name,action_type,to_chips):
        self.cur_hand[round_name].append((name, action_type, to_chips))

    def end_hand(self,result):
        self.cur_hand["result"] = result
        self.hands.append(self.cur_hand)
        self.cur_hand = None