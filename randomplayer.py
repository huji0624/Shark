#!/usr/bin/python

from shark.player import Player
import random


class randomPlayer(Player):
    def action(self, options , pot_chips):
        print options
        random_key = options.keys()[random.randint(0, len(options) - 1)]
        return random_key,options[random_key]
