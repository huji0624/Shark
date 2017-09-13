#!/usr/bin/python

from shark.player import Player
import random
from shark.action import *


class randomPlayer(Player):
    def action(self, options , info):
        key = None
        if PLAYER_ACTION_TYPE_ALLIN in options:
            rand = random.randint(0,100)
            if rand < 6:
                key = PLAYER_ACTION_TYPE_ALLIN
            else:
                keys = options.keys()
                keys.remove(PLAYER_ACTION_TYPE_ALLIN)
                key = keys[random.randint(0, len(keys) - 1)]
        else:
            key = options.keys()[random.randint(0, len(options) - 1)]
        # chips = 0
        # if key == PLAYER_ACTION_TYPE_RAISE:
        #     chips = random.randint(options[key],self.chips)
        return key,options[key]