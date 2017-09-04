#!/usr/bin/python

import player_state
from deuces import *
from log import *
from betround import *


class PlayerIns:
    def __init__(self, interface, chips):
        self.interface = interface
        self.hand_card = None
        self.hand_value = 0
        self.chips = chips
        self.state = None

    def hand_card_str(self):
        if self.hand_card:
            str = ""
            for card in self.hand_card:
                str = str + "," +Card.int_to_pretty_str(card)
            return str
        else:
            return ""

    def __repr__(self):
        return "name:%s||chips:%s||state:%s||handcard:%s||handvalue:%s" % (self.name, self.chips, self.state,self.hand_card_str(),self.hand_value)

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

    def player_with_name(self, name):
        for p in self.players:
            if p.name == name:
                return p
        return None

    def players_not_state(self, state):
        players_ = []
        for p in self.players:
            if p.state != state:
                players_.append(p)
        return players_

    def players_state(self,state):
        players_ = []
        for p in self.players:
            if p.state == state:
                players_.append(p)
        return players_

    def round_start(self):
        tmp_ = self.players.pop(0)
        self.players.append(tmp_)
        self.board = []
        self.deck = Deck()
        player_status = self.player_status()
        index = 0
        for p in self.players:
            hand_card = self.deck.draw(2)
            p.interface.roundStart(index , p.chips, hand_card, self.config , player_status)
            index =  index+1
            p.hand_card = hand_card
            p.state = player_state.PLAYER_STATE_ACTIVE
            logD("Player %s chips[%s] hand card:" % (p.interface.name, p.chips))
            Card.print_pretty_cards(p.hand_card)

    def player_status(self):
        player_status_map = {}
        index = 0
        for p in self.players:
            player_status_map[p.name] = {"position":index,"chips":p.chips}
            index = index + 1
        return player_status_map

    def round_end(self, result):
        for p in self.players:
            p.interface.roundEnd(result)
            if p.chips == 0:
                p.chips = self.config.buy_in
                self.rebuymap[p.name] = self.rebuymap[p.name] + 200

    def flop(self):
        cards = self.deck.draw(3)
        self.board.extend(cards)
        for p in self.players:
            p.interface.flop(cards)
        logD("Board:")
        Card.print_pretty_cards(self.board)

    def turn(self):
        card = self.deck.draw(1)
        self.board.append(card)
        for p in self.players:
            p.interface.turn(card)
        logD("Board:")
        Card.print_pretty_cards(self.board)

    def river(self):
        card = self.deck.draw(1)
        self.board.append(card)
        for p in self.players:
            p.interface.river(card)
        logD("Board:")
        Card.print_pretty_cards(self.board)

    def add_player(self, player):
        self.players.append(PlayerIns(player, self.config.buy_in))
        self.rebuymap[player.name] = 0

    def start(self):
        for p in self.players:
            p.interface.game_start(self.config)

    def end(self):
        for p in self.players:
            p.interface.game_end()

    def notify_action(self, action):
        for p in self.players:
            if p != action.player:
                p.interface.notify(action.player.name, action.type, action.chips, action.player.chips)
