#!/usr/bin/python

from shark import gameengine
from randomplayer import randomPlayer
from little_tight_player import LittleTightPlayer

from shark.game_config import *

ge = gameengine.GameEngine(GameConfig(50000, GAME_MODEL_RELEASE, GAME_LOG_LEVEL_DEBUG))

ge.addPlayer(LittleTightPlayer("tight"))
ge.addPlayer(randomPlayer("r1"))
ge.addPlayer(randomPlayer("r2"))
ge.addPlayer(randomPlayer("r3"))
ge.addPlayer(randomPlayer("r4"))
ge.addPlayer(randomPlayer("r5"))


ge.start()
