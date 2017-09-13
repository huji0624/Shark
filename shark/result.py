#!/usr/bin/python



class Result:
    def __init__(self, chips, hand_card, position):
        self.chips_gain = chips
        self.hand_card = hand_card
        self.position = position

    def __str__(self):
        return "chips + %s;" % self.chips_gain

    __repr__ = __str__
