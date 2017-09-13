#!/usr/bin/python

PLAYER_ACTION_TYPE_FOLD = "fold"
PLAYER_ACTION_TYPE_CHECK = "check"
PLAYER_ACTION_TYPE_CALL = "call"
PLAYER_ACTION_TYPE_RAISE = "raise"
PLAYER_ACTION_TYPE_ALLIN = "allin"
PLAYER_ACTION_TYPE_BB = "bb"
PLAYER_ACTION_TYPE_SB = "sb"


def SmallBlind(player, chips):
    ac = Action(PLAYER_ACTION_TYPE_SB)
    ac.player = player
    ac.chips = chips
    return ac


def BigBlind(player, chips):
    ac = Action(PLAYER_ACTION_TYPE_BB)
    ac.player = player
    ac.chips = chips
    return ac


def Fold(player):
    ac = Action(PLAYER_ACTION_TYPE_FOLD)
    ac.player = player
    return ac


'''
it means raise to actually.
'''


def Raise(player, chips):
    ac = Action(PLAYER_ACTION_TYPE_RAISE)
    ac.chips = chips
    ac.player = player
    return ac


def Call(player, chips):
    ac = Action(PLAYER_ACTION_TYPE_CALL)
    ac.chips = chips
    ac.player = player
    return ac


def Check(player):
    ac = Action(PLAYER_ACTION_TYPE_CHECK)
    ac.player = player
    return ac


def Allin(player, chips):
    ac = Action(PLAYER_ACTION_TYPE_ALLIN)
    ac.chips = chips
    ac.player = player
    return ac


class Action:
    def __init__(self, action_type):
        self.type = action_type
        self.chips = 0
        self.player = None
        self.un_action_player_count = 0

    def __repr__(self):
        return "type:%s||chips:%s||player:%s" % (self.type, self.chips, self.player.name)


class ActionInfo:
    def __init__(self, pot_chips, un_action_player_count):
        self.pot_chips = pot_chips
        self.need_action_player_count = un_action_player_count