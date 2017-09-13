#!/usr/bin/python


class Player:
    def __init__(self, name):
        self.name = name
        self.dealer = None
        self.chips = 0

    def game_start(self, config):
        pass

    def game_end(self):
        pass

    def roundStart(self, position, chips, handcard, desk_config, players):
        pass

    def flop(self, cards):
        pass

    def turn(self, card):
        pass

    def river(self, card):
        pass

    def roundEnd(self, result):
        pass

    def action(self, options, pot_chips):
        return None

    def notify(self, name, action_type, chips, leftchips):
        pass
