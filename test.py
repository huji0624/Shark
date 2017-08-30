#!/usr/bin/python

from deuces import *

evaluator = Evaluator()

p1 = [Card.new('9h'), Card.new('10j')]
print evaluator.evaluate(p1)
