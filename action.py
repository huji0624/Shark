#!/usr/bin/python

PLAYER_ACTION_TYPE_FOLD = "fold"
PLAYER_ACTION_TYPE_CHECK = "check"
PLAYER_ACTION_TYPE_CALL = "call"
PLAYER_ACTION_TYPE_RAISE = "raise"
PLAYER_ACTION_TYPE_ALLIN = "allin"

def Fold(player):
	ac = Action(PLAYER_ACTION_TYPE_FOLD)
	ac.player = player
	return ac

def Raise(player,chips):
	ac = Action(PLAYER_ACTION_TYPE_RAISE)
	ac.chips = chips
	ac.player = player
	return ac

def Call(player,chips):
	ac = Action(PLAYER_ACTION_TYPE_CALL)
	ac.chips = chips
	ac.player = player
	return ac

def Check(player):
	ac = Action(PLAYER_ACTION_TYPE_CHECK)
	ac.player = player
	return ac

def Allin(player,chips):
	ac = Action(PLAYER_ACTION_TYPE_ALLIN)
	ac.chips = chips
	ac.player = player
	return ac

class Action:
    def __init__(self, action_type):
        self.type = action_type
        self.chips = 0
        self.player = None

    def enough(self):
        if self.chips > self.player.chips:
            return False
        else:
            return True