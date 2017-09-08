#!/usr/bin/python


from deuces import *
from log import *
from action import *
import player_state


class BetRound:
    def __init__(self, round_name, pot, desk, pre_actions):
        self.round_name = round_name
        self.desk = desk
        self.pre_bets = pre_actions
        self.actions = []
        self.pot = pot
        if pre_actions:
            self.actions.extend(pre_actions)
        self.excuted_actions = []

    def excute_action(self, action):
        logD("==%s %s==chips[%s]" % (action.player.name, action.type, action.chips))
        if action.type == PLAYER_ACTION_TYPE_FOLD:
            action.player.state = player_state.PLAYER_STATE_FOLD
        elif action.type == PLAYER_ACTION_TYPE_ALLIN:
            action.player.chips = action.player.chips - (
                action.chips - self.pot.round_pot.bet_for_player(action.player))
            self.pot.set_bet(action.player, action.chips)
            action.player.state = player_state.PLAYER_STATE_ALLIN
        elif action.type == PLAYER_ACTION_TYPE_RAISE or action.type == PLAYER_ACTION_TYPE_CALL:
            if self.pot.round_pot.enough(action.player, action.chips):
                action.player.chips = action.player.chips - (
                    action.chips - self.pot.round_pot.bet_for_player(action.player))
                self.pot.set_bet(action.player, action.chips)
                action.player.state = player_state.PLAYER_STATE_ACTIVE
            else:
                logE("no enough chips for bet.")
        elif action.type == PLAYER_ACTION_TYPE_CHECK:
            action.player.state = player_state.PLAYER_STATE_ACTIVE
        elif action.type == PLAYER_ACTION_TYPE_BB:
            pass
        elif action.type == PLAYER_ACTION_TYPE_SB:
            pass
        else:
            logE("not support action." + action.type)
        self.excuted_actions.append(action)
        self.desk.notify_action(action)

    def next_action_player(self):
        pass

    def ask_for_action(self, player, un_action_count):
        pass

    def run(self):
        if len(self.actions) > 0:
            self.excute_action(self.actions.pop(0))
            return True
        else:
            action_player, count = self.next_action_player()
            if action_player:
                self.actions.append(self.ask_for_action(action_player, count))
                return True
            else:
                return False


class Dealer:
    def __init__(self):
        self.evaluator = Evaluator()
        # self.bet_rounds = []
        self.cur_bet_round = None

    def evaluate(self, hand, board):
        return self.evaluator.evaluate(hand, board)

    def new_bet_round(self, round_name, pot, desk, pre_actions):
        # if self.cur_bet_round:
        #     self.bet_rounds.append(self.cur_bet_round)
        pot.new_round_pot()
        self.cur_bet_round = BetRound(round_name, pot, desk, pre_actions)
        while True:
            if not self.cur_bet_round.run():
                break
        self.pot.cal_side_pot(self.cur_bet_round.excuted_actions)