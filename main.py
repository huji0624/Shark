#!/usr/bin/python

from shark import gameengine
from randomplayer import randomPlayer

ge = gameengine.gameEngine(100)

ge.addPlayer(randomPlayer("r1"))
ge.addPlayer(randomPlayer("r2"))
ge.addPlayer(randomPlayer("r3"))
ge.addPlayer(randomPlayer("r4"))
ge.addPlayer(randomPlayer("r5"))
ge.addPlayer(randomPlayer("r6"))

ge.game_start()
