#!/usr/bin/python

PLAYER_ACTION_TYPE_FOLD = "fold"
PLAYER_ACTION_TYPE_CHECK = "check"
PLAYER_ACTION_TYPE_CALL = "call"
PLAYER_ACTION_TYPE_RAISE = "raise"
PLAYER_ACTION_TYPE_ALLIN = "allin"


class action:
    def __init__(self, action_type):
        self.type = action_type
        self.chips = 0


class player:
    def name(self):
        return None

    def gameStart(self, buyin, bb, sb):
        pass

    def gameEnd(self):
        pass

    def roundStart(self, handcard):
        pass

    def roundEnd(self):
        pass

    def action(self, options, round_history):
        return None
