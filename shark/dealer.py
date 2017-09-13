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

    def round_will_start(self):
        self.pending_action_players = self.desk.players_state(player_state.PLAYER_STATE_ACTIVE)
        for p in self.pending_action_players:
            p.state = player_state.PLAYER_STATE_ACTION

    def excute_action(self, action):
        logD("==%s %s==chips[%s]" % (action.player.name, action.type, action.chips))
        if action.type == PLAYER_ACTION_TYPE_BB or action.type == PLAYER_ACTION_TYPE_SB:
            if action.chips >= action.player.chips:
                action.type = PLAYER_ACTION_TYPE_ALLIN
                action.chips = action.player.chips

        if action.type == PLAYER_ACTION_TYPE_FOLD:
            action.player.state = player_state.PLAYER_STATE_FOLD
            self.pending_action_players.remove(action.player)
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
        elif action.type == PLAYER_ACTION_TYPE_BB or action.type == PLAYER_ACTION_TYPE_SB:
            action.player.chips = action.player.chips - action.chips
            self.pot.set_bet(action.player, action.chips)
            action.player.state = player_state.PLAYER_STATE_ACTION
            cur_player = self.pending_action_players.pop(0)
            if cur_player == action.player:
                self.pending_action_players.append(cur_player)
            else:
                logE("some thing wrong with big blind.")
        else:
            logE("not support action." + action.type)
        self.excuted_actions.append(action)
        self.desk.notify_action(action)

    def next_action_player(self):
        player = self.pending_action_players.pop(0)
        count = len(self.pending_action_players)
        if player.state == player_state.PLAYER_STATE_ACTION:
            self.pending_action_players.append(player)
            return player,count
        elif player.state == player_state.PLAYER_STATE_ACTIVE:
            self.pending_action_players.append(player)
            if self.pot.round_pot.bet_for_player(player) == self.pot.round_pot.top():
                return None,count
            else:
                return player,count
        else:
            logE("error.no such player.")

    def ask_for_action(self, player, un_action_count):
        options = self.options_for_player(player)
        action_info = ActionInfo(self.pot.chips, un_action_count)
        (action_type, chips) = player.interface.action(options, action_info)
        # logD("action for player %s is %s,chips is %s" % (player.name, action_type, chips))
        if action_type not in options.keys():
            action_type = PLAYER_ACTION_TYPE_FOLD
        elif action_type == PLAYER_ACTION_TYPE_RAISE and chips >= player.chips:
            logI("raise more than he got.all in.")
            action_type = PLAYER_ACTION_TYPE_ALLIN
        elif action_type == PLAYER_ACTION_TYPE_CALL:
            chips = options[PLAYER_ACTION_TYPE_CALL]
        elif action_type == PLAYER_ACTION_TYPE_RAISE and chips < options[PLAYER_ACTION_TYPE_RAISE]:
            chips = options[PLAYER_ACTION_TYPE_RAISE]
        # prepare for action
        self.prepare_action(action_type, chips, player)

    def mini_raise(self):
        beforelastRaise = None
        lastRaise = None
        for i in range(len(self.excuted_actions) - 1, -1, -1):
            action = self.excuted_actions[i]
            if action.type == PLAYER_ACTION_TYPE_RAISE:
                if lastRaise == None:
                    lastRaise = action
                else:
                    beforelastRaise = action
                    break
        if beforelastRaise == None and lastRaise == None:
            return self.desk.config.big_blind
        elif beforelastRaise == None:
            return lastRaise.chips
        else:
            delta = lastRaise.chips - beforelastRaise.chips
            return delta if delta > self.desk.config.big_blind else self.desk.config.big_blind

    def options_for_player(self, player):
        top = self.pot.round_pot.top()
        options = {}
        if top == self.pot.round_pot.bet_for_player(player):
            options[PLAYER_ACTION_TYPE_CHECK] = 0
            options[PLAYER_ACTION_TYPE_RAISE] = self.desk.config.big_blind
            options[PLAYER_ACTION_TYPE_ALLIN] = player.chips
        else:
            options[PLAYER_ACTION_TYPE_FOLD] = 0
            if top >= player.chips + self.pot.round_pot.bet_for_player(player):
                options[PLAYER_ACTION_TYPE_ALLIN] = player.chips
            else:
                options[PLAYER_ACTION_TYPE_CALL] = top - self.pot.round_pot.bet_for_player(player)
                # the mini raise ask is how much more chips the amount player should give this time.
                options[PLAYER_ACTION_TYPE_RAISE] = top - self.pot.round_pot.bet_for_player(player) + self.mini_raise()
                options[PLAYER_ACTION_TYPE_ALLIN] = player.chips
        return options

    def append_action(self, action):
        self.actions.append(action)

    def prepare_action(self, action_type, chips, player):
        if action_type == PLAYER_ACTION_TYPE_FOLD:
            self.append_action(Fold(player))
        elif action_type == PLAYER_ACTION_TYPE_CHECK:
            self.append_action(Check(player))
        elif action_type == PLAYER_ACTION_TYPE_CALL:
            self.append_action(Call(player, chips + self.pot.round_pot.bet_for_player(player)))
        elif action_type == PLAYER_ACTION_TYPE_RAISE:
            self.append_action(Raise(player, chips + self.pot.round_pot.bet_for_player(player)))
        elif action_type == PLAYER_ACTION_TYPE_ALLIN:
            # if need allin.we need to deal with the side pot
            self.append_action(Allin(player, player.chips + self.pot.round_pot.bet_for_player(player)))
        else:
            logE("not support action." + action_type)

    def run(self):
        if len(self.actions) > 0:
            self.excute_action(self.actions.pop(0))
            return True
        else:
            action_player, count = self.next_action_player()
            if action_player:
                self.append_action(self.ask_for_action(action_player, count))
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

    @property
    def bet_round(self):
        return self.cur_bet_round

    def new_bet_round(self, round_name, pot, desk, pre_actions):
        # if self.cur_bet_round:
        #     self.bet_rounds.append(self.cur_bet_round)
        pot.new_round_pot()
        self.cur_bet_round = BetRound(round_name, pot, desk, pre_actions)
        self.cur_bet_round.round_will_start()

    def run_bet_round(self):
        while True:
            if not self.cur_bet_round.run():
                break
        self.pot.cal_side_pot(self.cur_bet_round.excuted_actions)