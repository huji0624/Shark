#!/usr/bin/python


from deuces import *
from bet_round import *
from pot import *


class Dealer:
    def __init__(self,desk):
        self.evaluator = Evaluator()
        # self.bet_rounds = []
        self.cur_bet_round = None
        self.desk = desk
        self.pot = None

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
        pass

    def show_hand_in_pot(self,pot_chips,players):
        pass
