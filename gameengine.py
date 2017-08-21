#!/usr/bin/python

from deuces import *

class gameEngine:
	def __init__(self):
		self.players = []
		self.bb = None
		
	def gameStart(self):
		while True:
			self.roundStart()
			self.roundEnd
	def addPlayer(self,player):
		self.players.append(player)

	def kickPlayer(self):
		pass
	def roundStart(self):
		self.deck = Deck()
		for p in self.players:
			p.roundStart()
		
	def roundEnd(self):
		pass