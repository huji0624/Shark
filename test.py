#!/usr/bin/python

from deuces import *

evaluator = Evaluator()

deck = Deck()
board = deck.draw(5)
print evaluator.evaluate(deck.draw(2),board)
