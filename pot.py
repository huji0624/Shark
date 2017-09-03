#!/usr/bin/python


import player_state


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
        final_action = {}
        for action in actions:
            final_action[action.player.name] = action
        final_active_actions = []
        for key, value in final_action.items():
            if value.player.state != player_state.PLAYER_STATE_FOLD:
                final_active_actions.append(value)
        tmp = {}
        for action_ in final_active_actions:
            tmp[action_.chips] = True
        if len(tmp) == 1:
            return
        sorted_actions = sorted(final_active_actions, key=lambda action_: action_.chips)
        while len(sorted_actions) > 0:
            first = sorted_actions.pop(0)
            if first.chips != 0:
                side_pot = SidePot(first.chips * len(sorted_actions) + first.chips)
                side_pot.add_player(first.player)
                for action_ in sorted_actions:
                    action_.chips = action_.chips - first.chips
                    side_pot.add_player(action_.player)
                self.round_pot.add_side_pot(side_pot)
