#!/usr/bin/python

class PlayerIns():
	def __init__(self,player):
		self.player = player
		self.handcard = None

from deuces import *
import random

class gameEngine:
	def __init__(self):
		self.players = []
		self.btn = None
		self.buyin = 200
		
	def gameStart(self):
		self.initGame()
		while True:
			self.roundStart()
			self.roundEnd

	def initGame(self):
		self.btn = random.randint(0,len(self.players) - 1)
		for p in self.players:
			p.player.gameStart(self.buyin)
			p.chips = self.buyin

	def addPlayer(self,player):
		self.players.append(PlayerIns(player))

	def kickPlayer(self):
		pass

	def roundStart(self):
		self.btn = self.btn + 1
		self.deck = Deck()
		for p in self.players:
			handcard = self.deck.draw(2)
			p.player.roundStart(handcard)
			p.handcard = handcard
		
	def roundEnd(self):
		self.deck = None
		for p in self.players:
			p.player.roundEnd()
		p.handcard = None