#!/usr/bin/python

from action import *
from log import *
from pot import *

STATE_ACTIVE = 0
STATE_FOLD = 1
STATE_ALLIN = 2


class Betround:
    def __init__(self, pot, desk):
        self.pot = pot
        self.desk = desk
        self.index = self.next(0)
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
                self.askForAction()
            if self.end():
                break
        # cal side pot
        self.pot.cal_side_pot(self.actions)

    def addExcutedAction(self, action):
        self.actions.append(action)

    def excuteAction(self, action):
        if action.type == PLAYER_ACTION_TYPE_FOLD:
            action.player.state = STATE_FOLD
        elif action.type == PLAYER_ACTION_TYPE_ALLIN:
            action.player.chips = action.player.chips - action.chips
            self.pot.set_bet(action.player,action.chips)
            self.addExcutedAction(action)
            action.player.state = STATE_ALLIN
        elif action.type == PLAYER_ACTION_TYPE_RAISE or action.type == PLAYER_ACTION_TYPE_CALL:
            logD("player %s chips[%s] , action %s chips %s" % (action.player.name,action.player.chips,action.type,action.chips))
            if self.pot.round_pot.enough(action.player,action.chips):
                action.player.chips = action.player.chips - action.chips
                self.pot.set_bet(action.player,action.chips)
                self.addExcutedAction(action)
            else:
                logE("no enough chips for bet.")
        elif action.type == PLAYER_ACTION_TYPE_CHECK:
            logD("player %s check.do nothing but move on." % (action.player.name))
        else:
            logE("not support action." + action.type)
        self.desk.notify_action(action)

    def nextActivePlayer(self):
        while True:
            p = self.desk.player_at_position(self.index)
            if p.state == STATE_ACTIVE:
                return p
            else:
                self.moveIndex()

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
            return lastRaise.chips - beforelastRaise.chips

    def askForAction(self):
        # this is not right.last action can be fold,raise,allin and the chips can be less than the retround
        curPlayer = self.nextActivePlayer()
        options = {}
        if self.pot.round_pot.chips == 0:
            options[PLAYER_ACTION_TYPE_CHECK] = True
            options[PLAYER_ACTION_TYPE_RAISE] = self.bigblind
            options[PLAYER_ACTION_TYPE_ALLIN] = curPlayer.chips
        else:
            options[PLAYER_ACTION_TYPE_FOLD] = True
            top = self.pot.round_pot.top()
            if top >= curPlayer.chips + self.pot.round_pot.bet_for_player(curPlayer):
                options[PLAYER_ACTION_TYPE_ALLIN] = curPlayer.chips
            else:
                options[PLAYER_ACTION_TYPE_CALL] = top - self.pot.round_pot.bet_for_player(curPlayer)
                #the mini raise ask is how much more chips the amount player should give this time.
                options[PLAYER_ACTION_TYPE_RAISE] = self.miniRaise()
                options[PLAYER_ACTION_TYPE_ALLIN] = True
        (action_type, chips) = curPlayer.interface.action(options)

        logD("action for player %s is %s,chips is %s" % (curPlayer.name, action_type, chips))

        if action_type not in options.keys():
            logE("return action is not in options.fold.")
            action_type = PLAYER_ACTION_TYPE_FOLD
        elif action_type == PLAYER_ACTION_TYPE_RAISE and chips >= curPlayer.chips:
            logI("raise more than he got.all in.")
            action_type = PLAYER_ACTION_TYPE_ALLIN
        elif action_type == PLAYER_ACTION_TYPE_CALL:
            chips = options[PLAYER_ACTION_TYPE_CALL]
        elif action_type == PLAYER_ACTION_TYPE_RAISE and chips < options[PLAYER_ACTION_TYPE_RAISE]:
            chips = options[PLAYER_ACTION_TYPE_RAISE]
        # prepare for action
        self.prepareAction(action_type, chips, curPlayer)

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

    def end(self):
        actives = self.desk.active_players()
        if len(actives) == 0:
            logE("no way.no active player.")
        elif len(actives) == 1:
            return True
        else:
            if self.pot.round_pot.even(actives):
                return True
            else:
                return False