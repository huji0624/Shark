#!/usr/bin/python


from shark.player import Player
from shark.action import *
from deuces import *
from shark.round_state import *


class StatisticsTightPlayer(Player):

    def game_start(self, config):
        self.hand_card = None
        self.hand_card_record = {}

    def roundStart(self, position, chips, handcard, desk_config, players):
        self.hand_card = handcard
        self.board = []

    def roundEnd(self, result):
        if self.name in result and result[self.name].chips_gain > 0:
            self.hand_card_record[self.hand_card_product()] = self.hand_card_product_value() + 2
        else:
            self.hand_card_record[self.hand_card_product()] = self.hand_card_product_value() - 2

    def hand_card_product(self):
        return Card.prime_product_from_hand(self.hand_card)

    def hand_card_product_value(self):
        return self.hand_card_record[self.hand_card_product()] if Card.prime_product_from_hand(self.hand_card) in self.hand_card_record else 100

    def flop(self, cards):
        self.board.extend(cards)

    def turn(self, card):
        self.board.append(card)

    def river(self, card):
        self.board.append(card)
    
    def action(self, options , info):
        if info.round_name != ROUND_STATE_PRE:
            value = self.dealer.evaluate(self.hand_card,self.board)
            if value <= 1599:
                return PLAYER_ACTION_TYPE_ALLIN,options[PLAYER_ACTION_TYPE_ALLIN]
            elif value <= 6185:
                if PLAYER_ACTION_TYPE_CHECK in options:
                    return PLAYER_ACTION_TYPE_CHECK,options[PLAYER_ACTION_TYPE_CHECK]
                elif PLAYER_ACTION_TYPE_CALL in options:
                    return PLAYER_ACTION_TYPE_CALL, options[PLAYER_ACTION_TYPE_CALL]
                else:
                    return PLAYER_ACTION_TYPE_ALLIN,options[PLAYER_ACTION_TYPE_ALLIN]
            else:
                return PLAYER_ACTION_TYPE_FOLD,0
        else:
            import random
            if random.randint(1,90) > self.hand_card_product_value():
                return PLAYER_ACTION_TYPE_FOLD,0
            else:
                if PLAYER_ACTION_TYPE_CALL in options:
                    return PLAYER_ACTION_TYPE_CALL,options[PLAYER_ACTION_TYPE_CALL]
                else:
                    return PLAYER_ACTION_TYPE_ALLIN, options[PLAYER_ACTION_TYPE_ALLIN]