#!/usr/bin/python

import gameengine
from randomplayer import randomPlayer

ge = gameengine.gameEngine()

ge.addPlayer(randomPlayer())
ge.addPlayer(randomPlayer())
ge.addPlayer(randomPlayer())
ge.addPlayer(randomPlayer())
ge.addPlayer(randomPlayer())
ge.addPlayer(randomPlayer())

ge.gameStart()