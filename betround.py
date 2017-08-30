#!/usr/bin/python

from player import *
from log import *


class Bet:
    def __init__(self, player, chips):
        self.player = player
        self.chips = chips

    def enough(self):
        if self.chips > self.player.chips:
            return False
        else:
            return True


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
        self.pendingbets = []
        self.bets = []

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
        self.pendingbets.append(Bet(self.players[self.index], chips))
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
            if len(self.pendingbets) > 0:
                self.excuteBet(self.pendingbets.pop(0))
            else:
                self.askForAction()
            if self.end():
                break

        #cal side pot
        for p in self.players:
            if p.state == STATE_ALLIN and p.sidepot==0:
                self.calSidePot(p)

        return self.roundpool

    def excuteBet(self, bet):
        if bet.enough():
            bet.player.chips = bet.player.chips - bet.chips
            self.roundpool = self.roundpool + bet.chips
            bet.player.roundbet = bet.player.roundbet + bet.chips
            self.bets.append(bet)
        else:
            logE("no enough chips for bet.")
            exit(1)

    def nextActivePlayer(self):
        while True:
            p = self.players[self.index]
            if p.state == STATE_ACTIVE:
                return p
            else:
                self.moveIndex()

    def askForAction(self):
        last = self.bets[-1]
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
        # do action
        self.actAction(ac, p)

    def actAction(self, action, player):
        if action.type == PLAYER_ACTION_TYPE_FOLD:
            player.state = STATE_FOLD
        elif action.type == PLAYER_ACTION_TYPE_CHECK:
            self.pendingbets.append(Bet(player, 0))
        elif action.type == PLAYER_ACTION_TYPE_CALL:
            self.pendingbets.append(Bet(player, action.lastbet.chips))
        elif action.type == PLAYER_ACTION_TYPE_RAISE:
            mini = 0
            if len(self.bets) == 0:
                mini = self.bigblind
            elif len(self.bets) == 1:
                mini = action.lastbet.chips
            else:
                mini = self.bets[-1].chips - self.bets[-2].chips
            if action.chips < mini:
                action.chips = mini
            self.pendingbets.append(Bet(player, action.chips))
        elif action.type == PLAYER_ACTION_TYPE_ALLIN:
            # if need allin.we need to deal with the side pot
            self.pendingbets.append(Bet(player, player.chips))
            player.state = STATE_ALLIN
        else:
            logE("not support action." + action.type)
            exit(1)

    def calSidePot(self,player):
        pass

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
