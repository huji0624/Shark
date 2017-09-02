#!/usr/bin/python

from player import player
import random


class randomPlayer(player):
    def action(self, options):
        random_key = options.keys()[random.randint(0, len(options) - 1)]
        return random_key,0
