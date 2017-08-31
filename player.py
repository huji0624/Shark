#!/usr/bin/python

class player:
    def __init__(self,name):
        self.name = name

    def gameStart(self, buyin, bb, sb):
        pass

    def gameEnd(self):
        pass

    def roundStart(self, handcard , players):
        pass

    def flop(self,cards):
    	pass

   	def turn(self,card):
   		pass

   	def river(self,card):
   		pass

    def roundEnd(self):
        pass

    def action(self, options):
        return None

    def notify(self, name, action_type, chips ,leftchips):
    	pass
