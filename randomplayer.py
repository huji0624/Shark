#!/usr/bin/python

from player import player
import random


class randomPlayer(player):
    def action(self, options , pot_chips):
        random_key = options.keys()[random.randint(0, len(options) - 1)]
        return random_key,options[random_key]
