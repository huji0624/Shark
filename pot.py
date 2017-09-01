#!/usr/bin/python


from action import *


class SidePot:
    def __init__(self, chips):
        self.chips = chips
        self.players = []

    def add_player(self, player):
        self.players.append(player)


class RoundPot:
    def __init__(self):
        self.player_bets = {}
        self.chips = 0

    @property
    def chips(self):
        return self.chips

    def enough(self, player, to_chips):
        if to_chips > (player.chips + self.player_bets[player.name]):
            return False
        else:
            return True

    def set_player_bet(self, player, bet):
        self.player_bets[player.name] = bet
        self.chips = 0
        for key, value in self.player_bets.items():
            self.chips = self.chips + value

    def top(self):
        tmp = 0
        for value in self.player_bets.values():
            if value > tmp:
                tmp = value
        return tmp

    def bet_for_player(self, player):
        return self.player_bets[player.name]

    def even(self, players):
        tmp = {}
        for p in players:
            tmp[self.player_bets[p.name]] = True
        if len(tmp) == 1:
            return True
        else:
            return False


class Pot:
    def __init__(self):
        self.chips = 0
        self.side_pots = []
        self.round_pot = None

    def new_round_pot(self):
        self.round_pot = RoundPot()

    @property
    def round_pot(self):
        return self.round_pot

    def set_bet(self, player, to_chips):
        self.round_pot.set_player_bet(player, to_chips)

    def add_side_pot(self, side_pot):
        self.side_pots.append(side_pot)

    def cal_side_pot(self):
        pass