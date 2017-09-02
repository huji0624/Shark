#!/usr/bin/python

from deuces import *
import random

print random.randint(0,3)

evaluator = Evaluator()

deck = Deck()
board = deck.draw(5)
print evaluator.evaluate(deck.draw(2), board)

acs = []
acs.append({"k": 4})
acs.append({"k": 2})
acs.append({"k": 3})
acs.append({"k": 1})
print sorted(acs,key=lambda d:d['k'])
