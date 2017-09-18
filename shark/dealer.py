#!/usr/bin/python


from deuces import *
from bet_round import *
from pot import *
from result import *


class Dealer:
    def __init__(self,desk):
        self.evaluator = Evaluator()
        # self.bet_rounds = []
        self.cur_bet_round = None
        self.desk = desk
        self.pot = None
        self.deal_get_chips = 0

    def evaluate(self, hand, board):
        return self.evaluator.evaluate(hand, board)

    @property
    def bet_round(self):
        return self.cur_bet_round

    def new_bet_round(self, round_name, pre_actions):
        # if self.cur_bet_round:
        #     self.bet_rounds.append(self.cur_bet_round)
        self.pot.new_round_pot()
        self.cur_bet_round = BetRound(round_name, self.pot, self.desk, pre_actions)
        self.cur_bet_round.round_will_start()

    def run_bet_round(self):
        while True:
            if not self.cur_bet_round.run():
                break
        self.pot.cal_side_pot(self.cur_bet_round.excuted_actions)

    def round_start(self):
        self.pot = Pot()

    def round_end(self):
        not_fold_players = self.desk.players_not_state(player_state.PLAYER_STATE_FOLD)
        not_fold_players_count = len(not_fold_players)
        if not_fold_players_count > 1:
            return self.show_hand(not_fold_players)
        elif not_fold_players_count == 1:
            return self.win(not_fold_players[0])
        else:
            logE("this can not happen.")

    def show_hand(self, not_fold_players):
        result = {}
        chips_gain_map = dict()
        for player in not_fold_players:
            chips_gain_map[player.name] = 0
            player.hand_value = self.evaluate(player.hand_card, self.desk.board)
        for round_pot_ in self.pot.round_pots:
            if round_pot_.has_side_pot():
                for side_pot in round_pot_.side_pots:
                    self.show_hand_in_pot(side_pot.chips, side_pot.players, chips_gain_map)
            else:
                self.show_hand_in_pot(round_pot_.chips, not_fold_players, chips_gain_map)
        for key, value in chips_gain_map.items():
            player = self.desk.player_with_name(key)
            result[key] = Result(value, player.hand_card, self.desk.players.index(player))
        logD("Result for round:======\n %s" % (result))
        return result

    def show_hand_in_pot(self, chips, players, chips_gain_map):
        tmp_players = []
        for p in players:
            if p.state != player_state.PLAYER_STATE_FOLD:
                tmp_players.append(p)
        players = tmp_players
        sorted_players = sorted(players, key=lambda player: player.hand_value)
        logD("show hand in round pot %s with player %s" % (chips, sorted_players))
        top_value_players = [sorted_players.pop(0)]
        for player in sorted_players:
            if player.hand_value == top_value_players[0].hand_value:
                top_value_players.append(player)
        top_count = len(top_value_players)
        chips = chips
        left = chips % top_count
        chips = chips - left
        each = chips / top_count
        self.deal_get_chips = self.deal_get_chips + left
        for player in top_value_players:
            player.chips = player.chips + each
            chips_gain_map[player.name] = chips_gain_map[player.name] + each

    def win(self, player):
        result = {}
        if player is None:
            logE("win player is None.")
        player.chips = player.chips + self.pot.chips
        result[player.name] = Result(self.pot.chips, None, self.desk.players.index(player))
        return result
