#!/usr/bin/python

from shark import gameengine
from randomplayer import randomPlayer

from shark.game_config import *

ge = gameengine.GameEngine(GameConfig(-1, GAME_MODEL_RELEASE, GAME_LOG_LEVEL_DEBUG))

ge.addPlayer(randomPlayer("r1"))
ge.addPlayer(randomPlayer("r2"))
ge.addPlayer(randomPlayer("r3"))
ge.addPlayer(randomPlayer("r4"))
ge.addPlayer(randomPlayer("r5"))
ge.addPlayer(randomPlayer("r6"))

ge.start()
