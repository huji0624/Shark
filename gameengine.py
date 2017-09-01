#!/usr/bin/python




from deuces import *
import random
import betround
from log import *
from pot import *
from desk import *


class gameEngine:
    def __init__(self):
        self.roundCount = 0
        self.desk = Desk(DeskConfig(200, 2, 1))
        self.pot = None

    def game_start(self):
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
        self.desk.start()

    def addPlayer(self, player):
        if player.name == None:
            print "add player fail.name must be set."
            return
        self.desk.add_player(player)

    def roundStart(self):
        self.roundCount = self.roundCount + 1
        self.desk.round_start()
        self.pot = Pot()
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
        self.desk.round_end(self.result)

    def showHand(self):
        show_hand_players = []
        evaluator = Evaluator()
        for p in self.players:
            if p != betround.STATE_FOLD:
                p.handvalue = evaluator.evaluate(p.handcard, self.board)
                show_hand_players.append(p)
                # [issue]refactor sidepot

    def win(self, player):
        if player == None:
            logE("win player is None.")
        player.chips = player.chips + self.pool
        self.pot = None

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
        pcount = len(self.desk.players)
        if pcount > 2:
            br = betround.Betround(self.pot, self.desk)
            br.addPreBet(self.desk.config.small_blind)
            br.addPreBet(self.desk.config.big_blind)
            br.loop()
        else:
            logE("not enough player.game stopped.")

    def flop(self):
        self.desk.flop()
        betround.Betround(self.pot, self.desk).loop()

    def turn(self):
        self.desk.turn()
        betround.Betround(self.pot, self.desk).loop()

    def river(self):
        self.desk.river()
        betround.Betround(self.pot, self.desk).loop()