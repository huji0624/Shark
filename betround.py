#!/usr/bin/python

from action import *
from log import *

STATE_ACTIVE = 0
STATE_FOLD = 1
STATE_ALLIN = 2


class Betround:
    def __init__(self, pool, players, button, bb):
        self.count = len(players)
        self.pool = pool
        self.roundpool = 0
        self.players = players
        self.index = self.next(button)
        self.bigblind = bb
        self.pendingactions = []
        self.actions = []

    def initall(self):
        for p in self.players:
            p.roundbet = 0

    def next(self, index):
        if index == (self.count - 1):
            return 0
        else:
            return index + 1

    def moveIndex(self):
        self.index = self.next(self.index)

    def addPreBet(self, chips):
        self.pendingactions.append(Raise(self.players[self.index], chips))
        self.moveIndex()

    def loop(self):
        self.initall()

        #check if there are active player.
        active_count = 0
        for p in self.players:
            if p.state == STATE_ACTIVE:
                active_count=active_count+1
        if active_count <= 1:
            return self.roundpool

        while True:
            if len(self.pendingactions) > 0:
                self.excuteAction(self.pendingactions.pop(0))
            else:
                self.askForAction()
            if self.end():
                break

        #cal side pot
        for p in self.players:
            if p.state == STATE_ALLIN and p.sidepot==0:
                self.calSidePot(p)

        return self.roundpool

    def addExcutedAction(self,action):
    	self.actions.append(action)

    def excuteAction(self, action):
    	if action.type == PLAYER_ACTION_TYPE_FOLD:
    		player.state = STATE_FOLD
    	elif action.type == PLAYER_ACTION_TYPE_ALLIN:
    		action.player.chips = action.player.chips - action.chips
			self.roundpool = self.roundpool + action.chips
			action.player.roundbet = action.player.roundbet + action.chips
			self.addExcutedAction(action)
			
    		player.state = STATE_ALLIN
    	elif action.type == PLAYER_ACTION_TYPE_RAISE or action.type == PLAYER_ACTION_TYPE_CALL:
    		if action.enough():
    			action.player.chips = action.player.chips - action.chips
    			self.roundpool = self.roundpool + action.chips
    			action.player.roundbet = action.player.roundbet + action.chips
    			self.addExcutedAction(action)
    		else:
    			logE("no enough chips for bet.")
    	elif action.type == PLAYER_ACTION_TYPE_CHECK:
    		logD("player %s check.do nothing but move on." % (action.player.name))
    	else:
    		logE("not support action." + action.type)
    	self.notifyAction(action)

    def notifyAction(self,action):
    	pass

    def nextActivePlayer(self):
        while True:
            p = self.players[self.index]
            if p.state == STATE_ACTIVE:
                return p
            else:
                self.moveIndex()

    def askForAction(self):
    	#this is not right.last action can be fold,raise,allin and the chips can be less than the retround
        last = self.actions[-1]
        p = self.nextActivePlayer()
        options = []
        if last.chips == 0:
            options.append(PLAYER_ACTION_TYPE_CHECK)
            options.append(PLAYER_ACTION_TYPE_RAISE)
            options.append(PLAYER_ACTION_TYPE_ALLIN)
        else:
            options.append(PLAYER_ACTION_TYPE_FOLD)
            if last.chips >= p.chips:
                options.append(PLAYER_ACTION_TYPE_ALLIN)
            else:
                options.append(PLAYER_ACTION_TYPE_CALL)
                options.append(PLAYER_ACTION_TYPE_RAISE)
                options.append(PLAYER_ACTION_TYPE_ALLIN)
        ac = p.player.action(options)
        ac.lastbet = last
        if ac.type not in options:
            logE("return action is not in options.fold.")
            ac.type = PLAYER_ACTION_TYPE_FOLD
        # prepare for action
        self.prepareAction(ac, p)

    def appendAction(self,action):
    	self.pendingactions.append(action)

    def prepareAction(self, action, player):
        if action.type == PLAYER_ACTION_TYPE_FOLD:
        	self.appendAction(Fold(player))
        elif action.type == PLAYER_ACTION_TYPE_CHECK:
            self.appendAction(Check(player))
        elif action.type == PLAYER_ACTION_TYPE_CALL:
            self.appendAction(Call(player, action.lastbet.chips))
        elif action.type == PLAYER_ACTION_TYPE_RAISE:
            mini = 0
            if len(self.bets) == 0:
                mini = self.bigblind
            elif len(self.bets) == 1:
                mini = action.lastbet.chips
            else:
            	#[issue] maybe we should search in the actions to find the mini raise
                mini = self.bets[-1].chips - self.bets[-2].chips
            if action.chips < mini:
                action.chips = mini
            self.appendAction(Raise(player, action.chips))
        elif action.type == PLAYER_ACTION_TYPE_ALLIN:
            # if need allin.we need to deal with the side pot
            self.appendAction(Allin(player, player.chips))
        else:
            logE("not support action." + action.type)

    def calSidePot(self,player):
        sidepot = 0
        for p in self.players:
        	if p.roundbet <= player.roundbet:
        		sidepot = sidepot + p.roundbet
        	else:
        		sidepot = sidepot + player.roundbet
        player.sidepot = sidepot

    def end(self):
        tmpmap = {}
        for p in self.players:
            if p.state == STATE_ALLIN:
                tmpmap[0] = True
            else:
                tmpmap[1] = True
        if len(tmpmap) == 1 and tmpmap[0] == True:
            return True

        tmpmap = {}
        for p in self.players:
            if p.state == STATE_ACTIVE:
                tmpmap[p.roundbet] = True
        if len(tmpmap) == 1:
            return True
        else:
            return False
