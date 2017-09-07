#!/usr/bin/python

import player_state
from deuces import *
from log import *
from betround import *
import game_config



DESK_STATE_NO = 0
DESK_STATE_PRE = 1
DESK_STATE_FLOP = 2
DESK_STATE_TURN = 3
DESK_STATE_RIVER = 4



class PlayerIns:
    def __init__(self, interface, chips):
        self.interface = interface
        self.hand_card = None
        self.hand_value = 0
        self.chips = chips
        self.state = None
        self.chips_gain = 0

    def hand_card_str(self):
        if self.hand_card:
            str = ""
            # for card in self.hand_card:
            #     str = str + "," +Card.int_to_pretty_str(card)
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
        self.desk_state = DESK_STATE_NO

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
            game_config.gg.hand_recorder.add_player(p.name, p.chips, p.hand_card)
            logD("Player %s chips[%s] hand card %s:" % (p.interface.name, p.chips, p.hand_card))
            if game_config.gg.is_log_level_debug:
                Card.print_pretty_cards(p.hand_card)
        self.desk_state = DESK_STATE_PRE

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
        self.desk_state = DESK_STATE_NO

    def flop(self):
        cards = self.deck.draw(3)
        for card in cards:
            game_config.gg.hand_recorder.add_board_card(card)
        self.board.extend(cards)
        for p in self.players:
            p.interface.flop(cards)
        if game_config.gg.is_log_level_debug:
            Card.print_pretty_cards(self.board)
        self.desk_state = DESK_STATE_FLOP

    def turn(self):
        card = self.deck.draw(1)
        game_config.gg.hand_recorder.add_board_card(card)
        self.board.append(card)
        for p in self.players:
            p.interface.turn(card)
        if game_config.gg.is_log_level_debug:
            Card.print_pretty_cards(self.board)
        self.desk_state = DESK_STATE_TURN

    def river(self):
        card = self.deck.draw(1)
        game_config.gg.hand_recorder.add_board_card(card)
        self.board.append(card)
        for p in self.players:
            p.interface.river(card)
        if game_config.gg.is_log_level_debug:
            Card.print_pretty_cards(self.board)
        self.desk_state = DESK_STATE_RIVER

    def add_player(self, player):
        self.players.append(PlayerIns(player, self.config.buy_in))

    def start(self):
        for p in self.players:
            p.interface.game_start(self.config)

    def end(self):
        for p in self.players:
            p.interface.game_end()

    def notify_action(self, action):
        recorder = game_config.gg.hand_recorder
        if self.desk_state == DESK_STATE_PRE:
            recorder.add_pre_flop_action(action.player.name,action.type,action.chips)
        elif self.desk_state == DESK_STATE_FLOP:
            recorder.add_flop_action(action.player.name, action.type, action.chips)
        elif self.desk_state == DESK_STATE_TURN:
            recorder.add_turn_action(action.player.name, action.type, action.chips)
        elif self.desk_state == DESK_STATE_RIVER:
            recorder.add_river_action(action.player.name, action.type, action.chips)
        else:
            logE("can not have action.")
        for p in self.players:
            if p != action.player:
                p.interface.notify(action.player.name, action.type, action.chips, action.player.chips)
