#!/usr/bin/python

from player import *
from log import *

class Bet:
	def __init__(self,player,chips):
		self.player = player
		self.chips = chips
	def enough(self):
		if self.chips > self.player.chips :
			return False
		else:
			return True

class Betround:
	def __init__(self,pool,players,button,bb):
		self.count = len(players)
		self.pool = pool
		self.roundpool = 0
		self.players = players
		self.index = self.next(button)
		self.bigblind = bb
		self.pendingbets = []
		self.bets = []

	def initall(self):
		for p in self.players:
			p.roundbet = 0

	def next(self,index):
		if index == (self.count - 1):
			return 0
		else:
			return index + 1

	def bet(self,chips):
		abet = Bet(self.players[self.index],chips)
		self.index = self.next(self.index)
		return abet

	def addPreBet(self,chips):
		self.pendingbets.append(self.bet(chips))

	def loop(self):
		self.initall()

		while True:
			if len(self.pendingbets)>0:
				self.excuteBet(self.pendingbets.pop(0))
			else:
				self.askForBet()
			if self.end():
				break 

		return self.roundpool + self.pool

	def excuteBet(self,bet):
		if bet.enough():
			bet.player.chips = bet.player.chips - bet.chips
			self.roundpool = self.roundpool + bet.chips
			bet.player.roundbet = bet.player.roundbet + bet.chips
			self.bets.append(bet)
		else:
			pass

	def askForBet(self):
		last = self.bets[-1]
		p = self.players[self.index]
		options = []
		if last.chips == 0:
			options.append(PLAYER_ACTION_TYPE_CHECK)
			options.append(PLAYER_ACTION_TYPE_RAISE)
			options.append(PLAYER_ACTION_TYPE_ALLIN)
		else:
			options.append(PLAYER_ACTION_TYPE_FOLD)
			if last.chips >= p.chips:
				options.append(PLAYER_ACTION_TYPE_ALLIN)
			else:
				options.append(PLAYER_ACTION_TYPE_CALL)
				options.append(PLAYER_ACTION_TYPE_RAISE)
				options.append(PLAYER_ACTION_TYPE_ALLIN)
		ac = p.player.action(options)
		if ac not in options:
			logerr("return action is not in options.fold.")
			ac = PLAYER_ACTION_TYPE_FOLD
		#do action


	def end(self):
		tmpmap = {}
		for p in self.players:
			tmpmap[p.roundbet] = True
		if len(tmpmap) == 1:
			return True
		else:
			return False		