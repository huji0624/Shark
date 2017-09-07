#!/usr/bin/python

from shark import gameengine
from randomplayer import randomPlayer
from little_tight_player import LittleTightPlayer

from shark.game_config import *

ge = gameengine.GameEngine(GameConfig(10, GAME_MODEL_RELEASE, GAME_LOG_LEVEL_DEBUG))

# ge.addPlayer(LittleTightPlayer("t1"))
# ge.addPlayer(LittleTightPlayer("t2"))
# ge.addPlayer(LittleTightPlayer("t3"))
# ge.addPlayer(LittleTightPlayer("t4"))
# ge.addPlayer(LittleTightPlayer("t5"))
# ge.addPlayer(LittleTightPlayer("t6"))
ge.addPlayer(randomPlayer("r1"))
ge.addPlayer(randomPlayer("r2"))
ge.addPlayer(randomPlayer("r3"))
ge.addPlayer(randomPlayer("r4"))
ge.addPlayer(randomPlayer("r5"))
ge.addPlayer(randomPlayer("r6"))


ge.start()
