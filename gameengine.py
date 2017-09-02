#!/usr/bin/python




from deuces import *
import random
import betround
from log import *
from pot import *
from desk import *


class Result:
    def __init__(self, chips, hand_card, position):
        self.chips_gain = chips
        self.hand_card = hand_card
        self.position = position


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
            if self.check_round():
                self.flop()
                if self.check_round():
                    self.turn()
                    if self.check_round():
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

    def check_round(self):
        if len(self.desk.players_not_state(STATE_FOLD)) == 1:
            return False
        else:
            return True

    def roundEnd(self):
        result = None
        not_fold_players = self.desk.players_not_state(STATE_FOLD)
        if len(not_fold_players) > 1:
            result = self.show_hand(not_fold_players)
        elif len(not_fold_players) == 1:
            result = self.win(not_fold_players[0])
        else:
            logE("this can not happen.")
        self.desk.round_end(result)

    def show_hand(self, not_fold_players):
        result = {}
        chips_gain_map = dict()
        evaluator_ = Evaluator()
        for player in not_fold_players:
            chips_gain_map[player] = 0
            player.hand_value = evaluator_.evaluate(player.hand_card, self.desk.board)
        for round_pot_ in self.pot.round_pots:
            if round_pot_.has_side_pot():
                for side_pot in round_pot_.side_pots:
                    self.show_hand_in_pot(side_pot.chips, side_pot.players, chips_gain_map)
            else:
                self.show_hand_in_pot(round_pot_.chips, not_fold_players, chips_gain_map)
        for key, value in chips_gain_map.items():
            result[key.name] = Result(value,key.hand_card,self.desk.players.index(key))
        return result

    def show_hand_in_pot(self, chips, players, chips_gain_map):
        sorted_players = sorted(players, key=lambda player: player.hand_value, reverse=True)
        top_value_players = [sorted_players.pop(0)]
        for player in sorted_players:
            if player.hand_value == top_value_players[0].hand_value:
                top_value_players.append(player)
        top_count = len(top_value_players)
        chips = chips
        left = chips % top_count
        chips = chips - left
        each = chips / top_count
        for player in top_value_players:
            player.chips = player.chips + each
            chips_gain_map[player] = chips_gain_map[player] + each

    def win(self, player):
        result = {}
        if player is None:
            logE("win player is None.")
        player.chips = player.chips + self.pot.chips
        result[player.name] = Result(self.pot.chips, None, self.desk.players.index(player))
        return self.pot.chips

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
