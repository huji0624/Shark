#!/usr/bin/python


from action import *


class SidePot:
    def __init__(self,chips):
        self.chips = chips
        self.players = []

    def add_player(self,player):
        self.players.append(player)


class Pot:
    def __init__(self):
        self.chips = 0
        self.side_pots = []

    def cal_side_pot_from_actions(self,actions):
        for action in actions:
            if action.type != PLAYER_ACTION_TYPE_FOLD:
                pass

    def add_side_pot(self,side_pot):
        self.side_pots.append(side_pot)