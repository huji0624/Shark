#!/usr/bin/python

class PlayerIns():
    def __init__(self, player):
        self.player = player
        self.handcard = None


from deuces import *
import random
import betround
from log import *


class gameEngine:
    def __init__(self):
        self.roundCount = 0
        self.players = []
        self.button = None
        self.buyin = 200
        self.bb = 2
        self.sb = 1
        self.board = None
        self.rebuymap = {}

    def gameStart(self):
        self.initGame()
        while True:
            self.roundStart()
            self.preFlop()
            if self.checkRound():
                self.flop()
                if self.checkRound():
                    self.turn()
                    if self.checkRound():
                        self.river()
            self.roundEnd()

    def initGame(self):
        self.button = random.randint(0, len(self.players) - 1)
        for p in self.players:
            p.player.gameStart(self.buyin, self.bb, self.sb)
            p.chips = self.buyin

    def addPlayer(self, player):
        if player.name == None:
            print "add player fail.name must be set."
            return
        self.players.append(PlayerIns(player))
        self.rebuymap[player.name] = 0

    def kickPlayer(self):
        pass

    def roundStart(self):
        self.roundCount = self.roundCount + 1
        self.button = self.button + 1
        self.deck = Deck()
        self.pool = 0
        self.board = []
        for p in self.players:
            if p.chips == 0:
                p.chips = self.buyin
                self.rebuymap[p.player.name] = self.rebuymap[p.player.name] + 200
            handcard = self.deck.draw(2)
            p.player.roundStart(handcard)
            p.handcard = handcard
            logD("Player %s handcard:%s" % (p.player.name, p.handcard))
        print "round %d start" % (self.roundCount)

    def roundEnd(self):
        if self.checkRound():
            self.showHand()
        else:
            active_player = None
            for p in self.players:
                if p.state != betround.STATE_FOLD:
                    active_player = p
                    break
            self.win(active_player)
        self.deck = None
        for p in self.players:
            p.player.roundEnd(self.result)
            p.handcard = None

    def showHand(self):
        pass

    def win(self,player):
        if player == None:
            logE("win player is None.")
        player.chips = player.chips + self.pool
        self.pool = 0

    def checkRound(self):
        fold_player_count = 0
        for p in self.players:
            if p.state == betround.STATE_FOLD:
                fold_player_count = fold_player_count + 1
        if fold_player_count == len(self.players) - 1:
            return False
        else:
            return True

    def preFlop(self):
        pcount = len(self.players)
        if pcount > 2:
            br = betround.Betround(0, self.players, self.button, self.bb)
            br.addPreBet(self.sb)
            br.addPreBet(self.bb)
            roundpool = br.loop()
            self.pool = self.pool + roundpool
        else:
            logE("not enough player.game stopped.")

    def flop(self):
        cards = self.deck.draw(3)
        self.board.extends(cards)
        for p in self.players:
            p.player.flop(cards)
        br = betround.Betround(0, self.players, self.button, self.bb)
        roundpool = br.loop()
        self.pool = self.pool + roundpool

    def turn(self):
        card = self.deck.draw(1)
        self.board.append(card)
        for p in self.players:
            p.player.turn(card)
        br = betround.Betround(0, self.players, self.button, self.bb)
        roundpool = br.loop()
        self.pool = self.pool + roundpool

    def river(self):
        card = self.deck.draw(1)
        self.board.append(card)
        for p in self.players:
            p.player.river(card)
        br = betround.Betround(0, self.players, self.button, self.bb)
        roundpool = br.loop()
        self.pool = self.pool + roundpool
