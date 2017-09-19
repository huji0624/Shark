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
        self.round_chips_record = {}

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
        players = self.desk.players
        for p in players:
            self.round_chips_record[p.name] = p.chips

    def round_end(self):
        not_fold_players = self.desk.players_not_state(player_state.PLAYER_STATE_FOLD)
        not_fold_players_count = len(not_fold_players)
        if not_fold_players_count > 1:
            return self.show_hand(not_fold_players)
        elif not_fold_players_count == 1:
            return self.win(not_fold_players[0])
        else:
            logE("this can not happen.")

    def gen_result(self,player_hand_cards):
        result = {}
        for p in self.desk.players:
            record_chips = self.round_chips_record[p.name]
            diff = p.chips - record_chips
            hand_card = player_hand_cards[p.name] if player_hand_cards is not None and p.name in player_hand_cards else None
            result[p.name] = Result(diff, hand_card, self.desk.players.index(p))
        logD("Result for round:======\n %s" % (result))
        return result

    def show_hand(self, not_fold_players):
        hand_cards = {}
        for player in not_fold_players:
            player.hand_value = self.evaluate(player.hand_card, self.desk.board)
            hand_cards[player.name] = player.hand_card
        for round_pot_ in self.pot.round_pots:
            if round_pot_.has_side_pot():
                for side_pot in round_pot_.side_pots:
                    self.show_hand_in_pot(side_pot.chips, side_pot.players)
            else:
                self.show_hand_in_pot(round_pot_.chips, not_fold_players)
        return self.gen_result(hand_cards)

    def show_hand_in_pot(self, chips, players):
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

    def win(self, player):
        if player is None:
            logE("win player is None.")
        player.chips = player.chips + self.pot.chips
        return self.gen_result(None)
