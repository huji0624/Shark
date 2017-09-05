#!/usr/bin/python


from shark.player import Player
from shark.action import *
from shark.deuces import *


class LittleTightPlayer(Player):

    def game_start(self, config):
        self.hand_card = None

    def roundStart(self, position, chips, handcard, desk_config, players):
        self.hand_card = handcard
        self.board = []

    def flop(self, cards):
        self.board.extend(cards)

    def turn(self, card):
        self.board.append(card)

    def river(self, card):
        self.board.append(card)
    
    def action(self, options , pot_chips):
        if len(self.board) >= 3:
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
            if PLAYER_ACTION_TYPE_CALL in options and options[PLAYER_ACTION_TYPE_CALL]<self.desk_config.big_blind*3:
                return PLAYER_ACTION_TYPE_CALL,options[PLAYER_ACTION_TYPE_CALL]
            else:
                return PLAYER_ACTION_TYPE_FOLD,0