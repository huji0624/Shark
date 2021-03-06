#!/usr/bin/python

from action import *
from log import *
import player_state


class Betround:
    def __init__(self, pot, desk, dealer):
        self.dealer = dealer
        self.pot = pot
        self.desk = desk
        self.index = 0
        self.pendingactions = []
        self.actions = []
        self.pot.new_round_pot()

    def init_all(self):
        actives = self.desk.players_state(player_state.PLAYER_STATE_ACTIVE)
        for p in actives:
            p.state = player_state.PLAYER_STATE_ACTION

    def next(self, index):
        if index == (self.desk.player_count - 1):
            return 0
        else:
            return index + 1

    def moveIndex(self):
        self.index = self.next(self.index)

    def addPreBet(self, chips):
        player = self.desk.player_at_position(self.index)
        if player.chips <= chips:
            self.excuteAction(Allin(player, player.chips))
        else:
            self.excuteAction(Raise(player, chips))
        self.moveIndex()

    def loop(self):
        self.init_all()
        # check if there are active player.
        if len(self.desk.players_state(player_state.PLAYER_STATE_ACTION)) <= 1:
            logD("no action player.just return.")
            return
        while 1:
            if len(self.pendingactions) > 0:
                self.excuteAction(self.pendingactions.pop(0))
            else:
                action_player = self.next_action_player()
                if action_player is None:
                    logD("no action player.break.")
                    break
                else:
                    self.ask_for_action(action_player)
        # cal side pot
        self.pot.cal_side_pot(self.actions)
        game_config.gg.hand_recorder.add_pot(self.pot.chips)


    def next_action_player(self):
        while 1:
            player = self.desk.player_at_position(self.index)
            if player.state == player_state.PLAYER_STATE_ACTION:
                not_fold_players = self.desk.players_not_state(PLAYER_ACTION_TYPE_FOLD)
                if len(not_fold_players) == 1 and not_fold_players[0] == player:
                    return None
                self.moveIndex()
                return player
            elif player.state == player_state.PLAYER_STATE_ACTIVE:
                if self.pot.round_pot.bet_for_player(player) < self.pot.round_pot.top():
                    self.moveIndex()
                    return player
                else:
                    if self.pot.round_pot.balance(self.desk.players_state(player_state.PLAYER_STATE_ACTIVE)):
                        return None
                    else:
                        self.moveIndex()
            else:
                if len(self.desk.players_state(player_state.PLAYER_STATE_ACTIVE)) == 0 and len(self.desk.players_state(player_state.PLAYER_STATE_ACTION)) == 0:
                    return None
                else:
                    self.moveIndex()

    def add_excuted_action(self, action):
        self.actions.append(action)

    def excuteAction(self, action):
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
        else:
            logE("not support action." + action.type)
        self.add_excuted_action(action)
        self.desk.notify_action(action)

    def miniRaise(self):
        beforelastRaise = None
        lastRaise = None
        for i in range(len(self.actions) - 1, -1, -1):
            action = self.actions[i]
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

    def ask_for_action(self, player):
        options = {}
        if self.pot.round_pot.chips == 0:
            options[PLAYER_ACTION_TYPE_CHECK] = True
            options[PLAYER_ACTION_TYPE_RAISE] = self.desk.config.big_blind
            options[PLAYER_ACTION_TYPE_ALLIN] = player.chips
        else:
            options[PLAYER_ACTION_TYPE_FOLD] = True
            top = self.pot.round_pot.top()
            if top >= player.chips + self.pot.round_pot.bet_for_player(player):
                options[PLAYER_ACTION_TYPE_ALLIN] = player.chips
            else:
                options[PLAYER_ACTION_TYPE_CALL] = top - self.pot.round_pot.bet_for_player(player)
                # the mini raise ask is how much more chips the amount player should give this time.
                options[PLAYER_ACTION_TYPE_RAISE] = top - self.pot.round_pot.bet_for_player(player) + self.miniRaise()
                options[PLAYER_ACTION_TYPE_ALLIN] = player.chips
        (action_type, chips) = player.interface.action(options, self.pot.chips)
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
        self.prepareAction(action_type, chips, player)

    def appendAction(self, action):
        self.pendingactions.append(action)

    def prepareAction(self, action_type, chips, player):
        if action_type == PLAYER_ACTION_TYPE_FOLD:
            self.appendAction(Fold(player))
        elif action_type == PLAYER_ACTION_TYPE_CHECK:
            self.appendAction(Check(player))
        elif action_type == PLAYER_ACTION_TYPE_CALL:
            self.appendAction(Call(player, chips + self.pot.round_pot.bet_for_player(player)))
        elif action_type == PLAYER_ACTION_TYPE_RAISE:
            self.appendAction(Raise(player, chips + self.pot.round_pot.bet_for_player(player)))
        elif action_type == PLAYER_ACTION_TYPE_ALLIN:
            # if need allin.we need to deal with the side pot
            self.appendAction(Allin(player, player.chips + self.pot.round_pot.bet_for_player(player)))
        else:
            logE("not support action." + action_type)
