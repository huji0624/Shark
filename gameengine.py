#!/usr/bin/python

class PlayerIns():
	def __init__(self,player):
		self.player = player
		self.handcard = None

from deuces import *
import random

class gameEngine:
	def __init__(self):
		self.roundCount = 0
		self.players = []
		self.button = None
		self.buyin = 200
		self.bb = 2
		self.sb = 1
		
	def gameStart(self):
		self.initGame()
		while True:
			self.roundStart()
			self.preFlop()
			self.flop()
			self.turn()
			self.river()
			self.roundEnd

	def initGame(self):
		self.button = random.randint(0,len(self.players) - 1)
		for p in self.players:
			p.player.gameStart(self.buyin,self.bb,self.sb)
			p.chips = self.buyin

	def addPlayer(self,player):
		if player.name() == None:
			print "add player fail.name must be set."
			return
		self.players.append(PlayerIns(player))

	def kickPlayer(self):
		pass

	def roundStart(self):
		self.roundCount = self.roundCount + 1
		self.button = self.button + 1
		self.deck = Deck()
		for p in self.players:
			handcard = self.deck.draw(2)
			p.player.roundStart(handcard)
			p.handcard = handcard
		print "round %d start" % (self.roundCount)
		
	def roundEnd(self):
		self.deck = None
		for p in self.players:
			p.player.roundEnd()
		p.handcard = None

	def preFlop(self):
		pcount = len(self.players)
		if pcount == 2:
			pass
		elif pcount > 2:
			pass
		else:
			print "only one player.game stopped."
			exit 1

	def flop(self):
		pass

	def turn(self):
		pass

	def river(self):
		pass