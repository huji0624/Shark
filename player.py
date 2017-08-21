#!/usr/bin/python

PLAYER_ACTION_TYPE_FOLD = "fold"
PLAYER_ACTION_TYPE_CHECK = "check"
PLAYER_ACTION_TYPE_CALL = "call"
PLAYER_ACTION_TYPE_RAISE = "raise"

class player:
	def gameStart(self):
		pass
	def gameEnd(self):
		pass
	def roundStart(self,handcard):
		pass
	def roundEnd(self):
		pass
	def action(self,round_history):
		return None