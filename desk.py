#!/usr/bin/python

import random
from deuces import *
from log import *
from betround import *


class PlayerIns:
    def __init__(self, interface, chips):
        self.interface = interface
        self.hand_card = None
        self.hand_value = 0
        self.chips = chips
        self.position = 0

    @property
    def name(self):
        return self.interface.name


class DeskConfig:
    def __init__(self, buy_in, big_blind, small_blind):
        self.buy_in = buy_in
        self.big_blind = big_blind
        self.small_blind = small_blind


class Desk:
    def __init__(self, config):
        self.players = []
        self.config = config
        self.board = None
        self.deck = None
        self.rebuymap = {}

    @property
    def player_count(self):
        return len(self.players)

    def player_at_position(self, index):
        return self.players[index]

    def active_player_count(self):
        return len(self.active_players())

    def active_players(self):
        actives = []
        for p in self.players:
            if p.state == STATE_ACTIVE:
                actives.append(p)
        return actives

    def players_not_state(self, state):
        players_ = []
        for p in self.players:
            if p.state != state:
                players_.append(p)
        return players_

    def round_start(self):
        tmp_ = self.players.pop()
        self.players.insert(0, tmp_)
        self.board = []
        self.deck = Deck()
        for p in self.players:
            if p.chips == 0:
                p.chips = self.config.buy_in
                self.rebuymap[p.player.name] = self.rebuymap[p.player.name] + 200
            hand_card = self.deck.draw(2)
            p.interface.roundStart(hand_card,None)
            p.hand_card = hand_card
            p.state = STATE_ACTIVE
            logD("Player %s chips[%s] hand card:%s" % (p.interface.name,p.chips, p.hand_card))

    def round_end(self, result):
        for p in self.players:
            p.interface.roundEnd(result)

    def flop(self):
        cards = self.deck.draw(3)
        self.board.extend(cards)
        for p in self.players:
            p.interface.flop(cards)

    def turn(self):
        card = self.deck.draw(1)
        self.board.append(card)
        for p in self.players:
            p.interface.turn(card)

    def river(self):
        card = self.deck.draw(1)
        self.board.append(card)
        for p in self.players:
            p.interface.river(card)

    def add_player(self, player):
        self.players.append(PlayerIns(player, self.config.buy_in))
        self.rebuymap[player.name] = 0

    def start(self):
        for p in self.players:
            p.interface.gameStart(self.config)

    def notify_action(self, action):
        for p in self.players:
            if p != action.player:
                p.interface.notify(action.player.name, action.type, action.chips, action.player.chips)
