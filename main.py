#!/usr/bin/python

from shark import gameengine
from randomplayer import randomPlayer
from little_tight_player import LittleTightPlayer

from shark.game_config import *

ge = gameengine.GameEngine(GameConfig(round_limit=10000, model=GAME_MODEL_RELEASE, log_level=GAME_LOG_LEVEL_NO,
                                      chips_model=GAME_CHIPS_MODEL_CLEAR,recorder_path=None))

ge.addPlayer(LittleTightPlayer("t1"))
# ge.addPlayer(LittleTightPlayer("t2"))
# ge.addPlayer(LittleTightPlayer("t3"))
# ge.addPlayer(LittleTightPlayer("t4"))
# ge.addPlayer(LittleTightPlayer("t5"))
# ge.addPlayer(LittleTightPlayer("t6"))
# ge.addPlayer(randomPlayer("r1"))
ge.addPlayer(randomPlayer("r2"))
ge.addPlayer(randomPlayer("r3"))
ge.addPlayer(randomPlayer("r4"))
ge.addPlayer(randomPlayer("r5"))
ge.addPlayer(randomPlayer("r6"))

ge.start()
