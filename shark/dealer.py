#!/usr/bin/python


from deuces import *


class Dealer:
    def __init__(self):
        self.evaluator = Evaluator()

    def evaluate(self, hand, board):
        return self.evaluator.evaluate(hand, board)