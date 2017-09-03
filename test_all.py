#!/usr/bin/python


import unittest
from action import *
from pot import *
from desk import *
from randomplayer import *


class Shark_Test_Side_Pot(unittest.TestCase):
    def setUp(self):
        self.p1 = PlayerIns(randomPlayer("p1"), 200)
        self.p2 = PlayerIns(randomPlayer("p2"), 200)
        self.p3 = PlayerIns(randomPlayer("p3"), 200)
        self.p4 = PlayerIns(randomPlayer("p4"), 200)
        self.p5 = PlayerIns(randomPlayer("p5"), 200)
        self.p6 = PlayerIns(randomPlayer("p6"), 200)

    def tearDown(self):
        pass

    def test_no_side_pot(self):
        actions = []
        actions.append(Raise(self.p1, 2))
        actions.append(Call(self.p2, 2))
        actions.append(Call(self.p3, 2))
        actions.append(Call(self.p4, 2))
        pot = Pot()
        pot.new_round_pot()
        pot.cal_side_pot(actions)
        self.assertEqual(len(pot.round_pot.side_pots), 0, "side pots wrong.")

    def test_side_pot_case_1(self):
        actions = []
        actions.append(Allin(self.p1, 1))
        actions.append(Call(self.p2, 2))
        actions.append(Call(self.p3, 2))
        actions.append(Call(self.p4, 2))
        actions.append(Fold(self.p5))
        pot = Pot()
        pot.new_round_pot()
        pot.cal_side_pot(actions)
        self.assertEqual(len(pot.round_pot.side_pots), 2)
        self.assertEqual(pot.round_pot.side_pots[0].chips, 4)
        self.assertEqual(pot.round_pot.side_pots[1].chips, 3)
        s0 = pot.round_pot.side_pots[0]
        self.assertIn(self.p1, s0.players)
        self.assertIn(self.p2, s0.players)
        self.assertIn(self.p3, s0.players)
        self.assertIn(self.p4, s0.players)
        s1 = pot.round_pot.side_pots[1]
        self.assertIn(self.p2, s1.players)
        self.assertIn(self.p3, s1.players)
        self.assertIn(self.p4, s1.players)

    def test_side_pot_case_2(self):
        actions = []
        actions.append(Raise(self.p1, 2))
        actions.append(Raise(self.p2, 40))
        actions.append(Allin(self.p3, 20))
        actions.append(Call(self.p4, 40))
        actions.append(Allin(self.p5,15))
        actions.append(Fold(self.p1))
        pot = Pot()
        pot.new_round_pot()
        pot.cal_side_pot(actions)
        self.assertEqual(len(pot.round_pot.side_pots), 3)
        self.assertEqual(pot.round_pot.side_pots[0].chips, 62)
        self.assertEqual(pot.round_pot.side_pots[1].chips, 15)
        self.assertEqual(pot.round_pot.side_pots[2].chips, 40)
        s0 = pot.round_pot.side_pots[0].players
        self.assertIn(self.p5, s0)
        self.assertIn(self.p2, s0)
        self.assertIn(self.p3, s0)
        self.assertIn(self.p4, s0)
        self.assertNotIn(self.p1,s0)
        s1 = pot.round_pot.side_pots[1].players
        self.assertIn(self.p2, s1)
        self.assertIn(self.p3, s1)
        self.assertIn(self.p4, s1)
        self.assertNotIn(self.p1, s1)
        self.assertNotIn(self.p5, s1)
        s2 = pot.round_pot.side_pots[2].players
        self.assertIn(self.p2, s2)
        self.assertIn(self.p4, s2)
        self.assertNotIn(self.p1, s2)
        self.assertNotIn(self.p3, s2)
        self.assertNotIn(self.p5, s2)

    def test_side_pot_case_3(self):
        actions = []
        actions.append(Raise(self.p3, 1))
        actions.append(Raise(self.p4, 2))
        actions.append(Allin(self.p5, 200))
        actions.append(Fold(self.p6))
        actions.append(Allin(self.p1,194))
        actions.append(Fold(self.p2))
        actions.append(Allin(self.p3,198))
        actions.append(Fold(self.p4))
        pot = Pot()
        pot.new_round_pot()
        pot.cal_side_pot(actions)
        self.assertEqual(len(pot.round_pot.side_pots), 3)
        self.assertEqual(pot.round_pot.side_pots[0].chips, 584)
        self.assertEqual(pot.round_pot.side_pots[1].chips, 8)
        self.assertEqual(pot.round_pot.side_pots[2].chips, 2)
        s0 = pot.round_pot.side_pots[0].players
        self.assertIn(self.p5, s0)
        self.assertIn(self.p1, s0)
        self.assertIn(self.p3, s0)
        self.assertNotIn(self.p4, s0)
        self.assertNotIn(self.p6,s0)
        self.assertNotIn(self.p2, s0)
        s1 = pot.round_pot.side_pots[1].players
        self.assertIn(self.p5, s1)
        self.assertIn(self.p3, s1)
        self.assertNotIn(self.p1, s1)
        self.assertNotIn(self.p2, s1)
        self.assertNotIn(self.p4, s1)
        self.assertNotIn(self.p6, s1)
        s2 = pot.round_pot.side_pots[2].players
        self.assertIn(self.p5, s2)
        self.assertNotIn(self.p4, s2)
        self.assertNotIn(self.p1, s2)
        self.assertNotIn(self.p3, s2)
        self.assertNotIn(self.p2, s2)
        self.assertNotIn(self.p6, s2)

    def test_side_pot_case_4(self):
        actions = []
        actions.append(Raise(self.p4, 1))
        actions.append(Raise(self.p5, 2))
        actions.append(Allin(self.p6,200))
        actions.append(Raise(self.p1, 202))
        actions.append(Allin(self.p2, 403))
        actions.append(Allin(self.p3, 197))
        actions.append(Fold(self.p4))
        actions.append(Fold(self.p5))
        actions.append(Fold(self.p1))
        pot = Pot()
        pot.new_round_pot()
        pot.cal_side_pot(actions)
        self.assertEqual(len(pot.round_pot.side_pots), 3)
        self.assertEqual(pot.round_pot.side_pots[0].chips, 3+197*4)
        self.assertEqual(pot.round_pot.side_pots[1].chips, 9)
        self.assertEqual(pot.round_pot.side_pots[2].chips, 205)
        s0 = pot.round_pot.side_pots[0].players
        self.assertIn(self.p3,s0)
        self.assertIn(self.p6, s0)
        self.assertIn(self.p2, s0)
        self.assertNotIn(self.p1, s0)
        self.assertNotIn(self.p5, s0)
        self.assertNotIn(self.p4, s0)
        s0 = pot.round_pot.side_pots[1].players
        self.assertIn(self.p2, s0)
        self.assertIn(self.p6, s0)
        self.assertNotIn(self.p1, s0)
        self.assertNotIn(self.p5, s0)
        self.assertNotIn(self.p3, s0)
        self.assertNotIn(self.p4, s0)
        s0 = pot.round_pot.side_pots[2].players
        self.assertIn(self.p2, s0)
        self.assertNotIn(self.p5, s0)
        self.assertNotIn(self.p1, s0)
        self.assertNotIn(self.p6, s0)
        self.assertNotIn(self.p3, s0)
        self.assertNotIn(self.p4, s0)

    def test_no_side_pot_case_2(self):
        actions = []
        actions.append(Raise(self.p2, 1))
        actions.append(Raise(self.p3, 2))
        actions.append(Fold(self.p4))
        actions.append(Allin(self.p5,200))
        actions.append(Allin(self.p6,200))
        actions.append(Fold(self.p1))
        actions.append(Fold(self.p2))
        actions.append(Fold(self.p3))
        pot = Pot()
        pot.new_round_pot()
        pot.cal_side_pot(actions)
        self.assertEqual(len(pot.round_pot.side_pots), 1)
        self.assertEqual(pot.round_pot.side_pots[0].chips,403)
        s0 = pot.round_pot.side_pots[0].players
        self.assertIn(self.p5,s0)
        self.assertIn(self.p6, s0)
        self.assertNotIn(self.p1, s0)
        self.assertNotIn(self.p2, s0)
        self.assertNotIn(self.p3, s0)
        self.assertNotIn(self.p4, s0)


unittest.main()
