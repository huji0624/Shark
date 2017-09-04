#!/usr/bin/python


import player_state
from action import *
from log import *


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
        self.side_pots = []

    def has_side_pot(self):
        if len(self.side_pots) == 0:
            return False
        else:
            return True

    def add_side_pot(self, side_pot):
        self.side_pots.append(side_pot)

    @property
    def chips(self):
        return self.chips

    def enough(self, player, to_chips):
        if to_chips > (player.chips + self.bet_for_player(player)):
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
        return self.player_bets[player.name] if self.player_bets.has_key(player.name) else 0

    def balance(self, players):
        for p in players:
            if self.bet_for_player(p) < self.top():
                return False
        return True


class Pot:
    def __init__(self):
        self.round_pot = None
        self.round_pots = []

    @property
    def chips(self):
        chips_ = 0
        for round_pot_ in self.round_pots:
            chips_ = chips_ + round_pot_.chips
        return chips_

    def new_round_pot(self):
        self.round_pot = RoundPot()
        self.round_pots.append(self.round_pot)

    @property
    def round_pot(self):
        return self.round_pot

    def set_bet(self, player, to_chips):
        self.round_pot.set_player_bet(player, to_chips)

    def cal_side_pot(self, actions):
        has_side_pot = False
        fold_players = []
        round_bets = {}
        for action in actions:
            if action.type == PLAYER_ACTION_TYPE_FOLD:
                fold_players.append(action.player.name)
            elif action.type == PLAYER_ACTION_TYPE_CHECK:
                round_bets[action.player.name] = action
            elif action.type == PLAYER_ACTION_TYPE_CALL:
                round_bets[action.player.name] = action
            elif action.type == PLAYER_ACTION_TYPE_RAISE:
                round_bets[action.player.name] = action
            elif action.type == PLAYER_ACTION_TYPE_ALLIN:
                round_bets[action.player.name] = action
                has_side_pot = True
            else:
                logE("not support type.")
        if has_side_pot:
            items = round_bets.values()
            sorted_items = sorted(items, key=lambda item_: item_.chips)
            side_chips = 0
            while len(sorted_items) > 0:
                item = sorted_items.pop(0)
                if item.player.name in fold_players:
                    side_chips = side_chips + item.chips
                else:
                    if item.chips != 0:
                        side_pot = SidePot(item.chips * len(sorted_items) + item.chips + side_chips)
                        side_chips = 0
                        side_pot.add_player(item.player)
                        for action_ in sorted_items:
                            action_.chips = action_.chips - item.chips
                            if action_.player.name not in fold_players:
                                side_pot.add_player(action_.player)
                        self.round_pot.add_side_pot(side_pot)
        else:
            return
