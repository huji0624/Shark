#!/usr/bin/python

from action import *
from log import *
from pot import *

STATE_ACTIVE = "active"
STATE_FOLD = "fold"
STATE_ALLIN = "allin"


class Betround:
    def __init__(self, pot, desk):
        self.pot = pot
        self.desk = desk
        self.index = 0
        self.pendingactions = []
        self.actions = []

    def initall(self):
        self.pot.new_round_pot()

    def next(self, index):
        if index == (self.desk.player_count - 1):
            return 0
        else:
            return index + 1

    def moveIndex(self):
        self.index = self.next(self.index)

    def addPreBet(self, chips):
        self.pendingactions.append(Raise(self.desk.player_at_position(self.index), chips))
        self.moveIndex()

    def loop(self):
        self.initall()
        # check if there are active player.
        if self.desk.active_player_count() <= 1:
            return
        while True:
            if len(self.pendingactions) > 0:
                self.excuteAction(self.pendingactions.pop(0))
            else:
                action_player = self.next_action_player()
                if action_player is None:
                    break
                else:
                    self.ask_for_action(action_player)
        # cal side pot
        self.pot.cal_side_pot(self.actions)

    def next_action_player(self):
        while True:
            player = self.desk.player_at_position(self.index)
            if player.state == STATE_ACTIVE and self.pot.round_pot.bet_for_player(player) < self.pot.round_pot.top():
                self.moveIndex()
                return player
            else:
                actives = self.desk.active_players()
                actives_not_even = self.pot.round_pot.not_even(actives)
                print len(actives_not_even)
                if len(actives_not_even) == 0:
                    return None
                else:
                    self.moveIndex()

    def addExcutedAction(self, action):
        self.actions.append(action)

    def excuteAction(self, action):
        logD("==%s %s==chips[%s]" % (action.player.name, action.type, action.chips))
        if action.type == PLAYER_ACTION_TYPE_FOLD:
            action.player.state = STATE_FOLD
        elif action.type == PLAYER_ACTION_TYPE_ALLIN:
            action.player.chips = action.player.chips - action.chips
            self.pot.set_bet(action.player, action.chips)
            self.addExcutedAction(action)
            action.player.state = STATE_ALLIN
        elif action.type == PLAYER_ACTION_TYPE_RAISE or action.type == PLAYER_ACTION_TYPE_CALL:
            if self.pot.round_pot.enough(action.player, action.chips):
                action.player.chips = action.player.chips - action.chips
                self.pot.set_bet(action.player, action.chips)
                self.addExcutedAction(action)
            else:
                logE("no enough chips for bet.")
        elif action.type == PLAYER_ACTION_TYPE_CHECK:
            pass
        else:
            logE("not support action." + action.type)
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
            return self.bigblind
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
                options[PLAYER_ACTION_TYPE_RAISE] = self.miniRaise()
                options[PLAYER_ACTION_TYPE_ALLIN] = True
        (action_type, chips) = player.interface.action(options)

        logD("action for player %s is %s,chips is %s" % (player.name, action_type, chips))

        if action_type not in options.keys():
            logE("return action is not in options.fold.")
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