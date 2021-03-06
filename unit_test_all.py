#!/usr/bin/python


import unittest
from shark.action import *
from shark.pot import *
from shark.desk import *
from shark.dealer import *
from randomplayer import *


class Shark_Test(unittest.TestCase):
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

    def test_dealer_pre_flop_1(self):
        self.desk = Desk(DeskConfig(200, 2, 1))
        self.desk.players = [self.p1, self.p2, self.p3, self.p4]
        for p in self.desk.players:
            p.state = player_state.PLAYER_STATE_ACTIVE
        self.dealer = Dealer()
        pres = [SmallBlind(self.p1,1),BigBlind(self.p2,2)]
        self.dealer.new_bet_round("pre_flop",Pot(),self.desk,pres)
        br = self.dealer.bet_round
        br.run()
        br.run()
        p,count = br.next_action_player()
        self.assertEqual(p,self.p3)
        self.assertEqual(count,3)
        options = br.options_for_player(p)
        self.assertIn(PLAYER_ACTION_TYPE_ALLIN,options)
        self.assertIn(PLAYER_ACTION_TYPE_FOLD, options)
        self.assertIn(PLAYER_ACTION_TYPE_CALL, options)
        self.assertIn(PLAYER_ACTION_TYPE_RAISE, options)
        self.assertNotIn(PLAYER_ACTION_TYPE_CHECK, options)
        self.assertEqual(options[PLAYER_ACTION_TYPE_RAISE],4)
        self.assertEqual(options[PLAYER_ACTION_TYPE_CALL], 2)
        self.assertEqual(options[PLAYER_ACTION_TYPE_ALLIN], 200)
        br.excute_action(Call(self.p3,2))
        p, count = br.next_action_player()
        self.assertEqual(p,self.p4)
        self.assertEqual(count, 3)
        br.excute_action(Call(self.p4,2))
        p,count = br.next_action_player()
        self.assertEqual(p, self.p1)
        self.assertEqual(count, 3)
        options = br.options_for_player(p)
        self.assertIn(PLAYER_ACTION_TYPE_ALLIN, options)
        self.assertIn(PLAYER_ACTION_TYPE_FOLD, options)
        self.assertIn(PLAYER_ACTION_TYPE_CALL, options)
        self.assertIn(PLAYER_ACTION_TYPE_RAISE, options)
        self.assertNotIn(PLAYER_ACTION_TYPE_CHECK, options)
        self.assertEqual(options[PLAYER_ACTION_TYPE_RAISE], 3)
        self.assertEqual(options[PLAYER_ACTION_TYPE_CALL], 1)
        self.assertEqual(options[PLAYER_ACTION_TYPE_ALLIN], 199)
        br.excute_action(Call(self.p1, 2))
        p,count = br.next_action_player()
        self.assertEqual(p, self.p2)
        self.assertEqual(count, 3)
        options = br.options_for_player(p)
        self.assertIn(PLAYER_ACTION_TYPE_ALLIN, options)
        self.assertIn(PLAYER_ACTION_TYPE_CHECK, options)
        self.assertIn(PLAYER_ACTION_TYPE_RAISE, options)
        self.assertNotIn(PLAYER_ACTION_TYPE_FOLD, options)
        self.assertNotIn(PLAYER_ACTION_TYPE_CALL, options)
        self.assertEqual(options[PLAYER_ACTION_TYPE_RAISE], 2)
        self.assertEqual(options[PLAYER_ACTION_TYPE_ALLIN], 198)
        br.excute_action(Check(self.p2))
        p,count = br.next_action_player()
        self.assertIsNone(p)

    def test_dealer_pre_flop_2(self):
        self.desk = Desk(DeskConfig(200, 2, 1))
        self.desk.players = [self.p1, self.p2, self.p3, self.p4]
        for p in self.desk.players:
            p.state = player_state.PLAYER_STATE_ACTIVE
        self.dealer = Dealer()
        pres = [SmallBlind(self.p1,1),BigBlind(self.p2,2)]
        self.dealer.new_bet_round("pre_flop",Pot(),self.desk,pres)
        br = self.dealer.bet_round
        br.run()
        br.run()
        p,count = br.next_action_player()
        self.assertEqual(p,self.p3)
        self.assertEqual(count,3)
        options = br.options_for_player(p)
        self.assertIn(PLAYER_ACTION_TYPE_ALLIN,options)
        self.assertIn(PLAYER_ACTION_TYPE_FOLD, options)
        self.assertIn(PLAYER_ACTION_TYPE_CALL, options)
        self.assertIn(PLAYER_ACTION_TYPE_RAISE, options)
        self.assertNotIn(PLAYER_ACTION_TYPE_CHECK, options)
        self.assertEqual(options[PLAYER_ACTION_TYPE_RAISE],4)
        self.assertEqual(options[PLAYER_ACTION_TYPE_CALL], 2)
        self.assertEqual(options[PLAYER_ACTION_TYPE_ALLIN], 200)
        br.excute_action(Fold(p))
        #p4
        p, count = br.next_action_player()
        self.assertEqual(p,self.p4)
        self.assertEqual(count, 2)
        br.excute_action(Fold(self.p4))
        #p1
        p,count = br.next_action_player()
        self.assertEqual(p, self.p1)
        self.assertEqual(count, 1)
        options = br.options_for_player(p)
        self.assertIn(PLAYER_ACTION_TYPE_ALLIN, options)
        self.assertIn(PLAYER_ACTION_TYPE_FOLD, options)
        self.assertIn(PLAYER_ACTION_TYPE_CALL, options)
        self.assertIn(PLAYER_ACTION_TYPE_RAISE, options)
        self.assertNotIn(PLAYER_ACTION_TYPE_CHECK, options)
        self.assertEqual(options[PLAYER_ACTION_TYPE_RAISE], 3)
        self.assertEqual(options[PLAYER_ACTION_TYPE_CALL], 1)
        self.assertEqual(options[PLAYER_ACTION_TYPE_ALLIN], 199)
        br.excute_action(Fold(self.p1))
        #p2
        p,count = br.next_action_player()
        self.assertIsNone(p)

    def test_dealer_pre_flop_3(self):
        self.desk = Desk(DeskConfig(200, 2, 1))
        self.desk.players = [self.p1, self.p2, self.p3, self.p4]
        for p in self.desk.players:
            p.state = player_state.PLAYER_STATE_ACTIVE
        self.dealer = Dealer()
        pres = [SmallBlind(self.p1,1),BigBlind(self.p2,2)]
        self.dealer.new_bet_round("pre_flop",Pot(),self.desk,pres)
        br = self.dealer.bet_round
        br.run()
        br.run()
        #p3
        p,count = br.next_action_player()
        self.assertEqual(p,self.p3)
        self.assertEqual(count,3)
        options = br.options_for_player(p)
        self.assertIn(PLAYER_ACTION_TYPE_ALLIN,options)
        self.assertIn(PLAYER_ACTION_TYPE_FOLD, options)
        self.assertIn(PLAYER_ACTION_TYPE_CALL, options)
        self.assertIn(PLAYER_ACTION_TYPE_RAISE, options)
        self.assertNotIn(PLAYER_ACTION_TYPE_CHECK, options)
        self.assertEqual(options[PLAYER_ACTION_TYPE_RAISE],4)
        self.assertEqual(options[PLAYER_ACTION_TYPE_CALL], 2)
        self.assertEqual(options[PLAYER_ACTION_TYPE_ALLIN], 200)
        br.excute_action(Allin(p,200))
        #p4
        p, count = br.next_action_player()
        self.assertEqual(p,self.p4)
        self.assertEqual(count, 2)
        br.excute_action(Fold(self.p4))
        #p1
        p,count = br.next_action_player()
        self.assertEqual(p, self.p1)
        self.assertEqual(count, 1)
        options = br.options_for_player(p)
        self.assertIn(PLAYER_ACTION_TYPE_ALLIN, options)
        self.assertIn(PLAYER_ACTION_TYPE_FOLD, options)
        self.assertNotIn(PLAYER_ACTION_TYPE_CALL, options)
        self.assertNotIn(PLAYER_ACTION_TYPE_RAISE, options)
        self.assertNotIn(PLAYER_ACTION_TYPE_CHECK, options)
        self.assertEqual(options[PLAYER_ACTION_TYPE_ALLIN], 199)
        br.excute_action(Fold(p))
        #p2
        p,count = br.next_action_player()
        self.assertIsNotNone(p)


    def test_dealer_flop_1(self):
        self.desk = Desk(DeskConfig(200, 2, 1))
        self.desk.players = [self.p1, self.p2, self.p3, self.p4]
        for p in self.desk.players:
            p.state = player_state.PLAYER_STATE_ACTIVE
        self.dealer = Dealer()
        pot = Pot()
        self.dealer.new_bet_round("flop",pot,self.desk,None)
        br = self.dealer.bet_round
        #p1===
        p,count = br.next_action_player()
        self.assertEqual(p,self.p1)
        self.assertEqual(count,3)
        options = br.options_for_player(p)
        self.assertIn(PLAYER_ACTION_TYPE_ALLIN, options)
        self.assertIn(PLAYER_ACTION_TYPE_CHECK, options)
        self.assertIn(PLAYER_ACTION_TYPE_RAISE, options)
        self.assertNotIn(PLAYER_ACTION_TYPE_FOLD, options)
        self.assertNotIn(PLAYER_ACTION_TYPE_CALL, options)
        self.assertEqual(options[PLAYER_ACTION_TYPE_RAISE], 2)
        self.assertEqual(options[PLAYER_ACTION_TYPE_CHECK], 0)
        self.assertEqual(options[PLAYER_ACTION_TYPE_ALLIN], 200)
        br.excute_action(Check(self.p1))
        # p2===
        p, count = br.next_action_player()
        self.assertEqual(p, self.p2)
        self.assertEqual(count, 3)
        options = br.options_for_player(p)
        self.assertIn(PLAYER_ACTION_TYPE_ALLIN, options)
        self.assertIn(PLAYER_ACTION_TYPE_CHECK, options)
        self.assertIn(PLAYER_ACTION_TYPE_RAISE, options)
        self.assertNotIn(PLAYER_ACTION_TYPE_FOLD, options)
        self.assertNotIn(PLAYER_ACTION_TYPE_CALL, options)
        self.assertEqual(options[PLAYER_ACTION_TYPE_RAISE], 2)
        self.assertEqual(options[PLAYER_ACTION_TYPE_CHECK], 0)
        self.assertEqual(options[PLAYER_ACTION_TYPE_ALLIN], 200)
        br.excute_action(Raise(self.p2,8))
        self.assertEqual(self.p2.chips,192)
        # p3===
        p, count = br.next_action_player()
        self.assertEqual(p, self.p3)
        self.assertEqual(count, 3)
        options = br.options_for_player(p)
        self.assertIn(PLAYER_ACTION_TYPE_CALL, options)
        self.assertIn(PLAYER_ACTION_TYPE_ALLIN, options)
        self.assertIn(PLAYER_ACTION_TYPE_RAISE, options)
        self.assertIn(PLAYER_ACTION_TYPE_FOLD, options)
        self.assertNotIn(PLAYER_ACTION_TYPE_CHECK, options)
        self.assertEqual(options[PLAYER_ACTION_TYPE_RAISE], 16)
        self.assertEqual(options[PLAYER_ACTION_TYPE_CALL], 8)
        self.assertEqual(options[PLAYER_ACTION_TYPE_ALLIN], 200)
        br.excute_action(Raise(p, 24))
        self.assertEqual(self.p3.chips, 176)
        # p4===
        p, count = br.next_action_player()
        self.assertEqual(p, self.p4)
        self.assertEqual(count, 3)
        options = br.options_for_player(p)
        self.assertIn(PLAYER_ACTION_TYPE_CALL, options)
        self.assertIn(PLAYER_ACTION_TYPE_ALLIN, options)
        self.assertIn(PLAYER_ACTION_TYPE_RAISE, options)
        self.assertIn(PLAYER_ACTION_TYPE_FOLD, options)
        self.assertNotIn(PLAYER_ACTION_TYPE_CHECK, options)
        self.assertEqual(options[PLAYER_ACTION_TYPE_RAISE], 40)
        self.assertEqual(options[PLAYER_ACTION_TYPE_CALL], 24)
        self.assertEqual(options[PLAYER_ACTION_TYPE_ALLIN], 200)
        br.excute_action(Allin(p, 200))
        self.assertEqual(p.chips, 0)
        # p1===
        p, count = br.next_action_player()
        self.assertEqual(p, self.p1)
        self.assertEqual(count, 2)
        options = br.options_for_player(p)
        self.assertIn(PLAYER_ACTION_TYPE_ALLIN, options)
        self.assertIn(PLAYER_ACTION_TYPE_FOLD, options)
        self.assertNotIn(PLAYER_ACTION_TYPE_CHECK, options)
        self.assertNotIn(PLAYER_ACTION_TYPE_RAISE, options)
        self.assertNotIn(PLAYER_ACTION_TYPE_CALL, options)
        self.assertEqual(options[PLAYER_ACTION_TYPE_ALLIN], 200)
        br.excute_action(Fold(p))
        self.assertEqual(p.chips, 200)
        # p2===
        p, count = br.next_action_player()
        self.assertEqual(p, self.p2)
        self.assertEqual(count, 1)
        options = br.options_for_player(p)
        self.assertIn(PLAYER_ACTION_TYPE_ALLIN, options)
        self.assertIn(PLAYER_ACTION_TYPE_FOLD, options)
        self.assertNotIn(PLAYER_ACTION_TYPE_CHECK, options)
        self.assertNotIn(PLAYER_ACTION_TYPE_RAISE, options)
        self.assertNotIn(PLAYER_ACTION_TYPE_CALL, options)
        self.assertEqual(options[PLAYER_ACTION_TYPE_ALLIN], 192)
        br.excute_action(Allin(p,200))
        self.assertEqual(p.chips, 0)
        # p3===
        p, count = br.next_action_player()
        self.assertEqual(p, self.p3)
        self.assertEqual(count, 0)
        options = br.options_for_player(p)
        self.assertIn(PLAYER_ACTION_TYPE_ALLIN, options)
        self.assertIn(PLAYER_ACTION_TYPE_FOLD, options)
        self.assertNotIn(PLAYER_ACTION_TYPE_CHECK, options)
        self.assertNotIn(PLAYER_ACTION_TYPE_RAISE, options)
        self.assertNotIn(PLAYER_ACTION_TYPE_CALL, options)
        self.assertEqual(options[PLAYER_ACTION_TYPE_ALLIN], 176)
        br.excute_action(Fold(p))
        self.assertEqual(p.chips, 176)
        self.assertEqual(pot.chips,424)
        #no action player
        p, count = br.next_action_player()
        self.assertIsNone(p)


unittest.main()
