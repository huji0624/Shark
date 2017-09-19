#!/usr/bin/python


from shark.player import Player
from shark.action import *
from deuces import *
from shark.round_state import *
import shark.game_config


class HandsSta:
    def __init__(self):
        pass


class HandValue:
    def __init__(self):
        self.value = None
        self.hands = None



class StatisticsTightPlayer(Player):

    def game_start(self, config):
        self.hand_card = None
        self.hand_card_record = {}
        self.count = 0

    def roundStart(self, position, chips, handcard, desk_config, players):
        self.hand_card = handcard
        self.board = []
        self.count = self.count + 1

    def roundEnd(self, result):
        if self.name in result and result[self.name].chips_gain > 0:
            self.hand_card_record[self.hand_card_product()] = self.hand_card_product_value() + 2
        else:
            to = self.hand_card_product_value() - 1
            if to <= 0:
                self.hand_card_record[self.hand_card_product()] = 20
            else:
                self.hand_card_record[self.hand_card_product()] = to

        if self.count%10000==0:
            self.handsta()

    def game_end(self):
        self.handsta()

    def handsta(self):
        res = ""
        items = self.hand_card_record.items()
        sorted_items = sorted(items,key=lambda i: i[1])
        prime_map = {}
        for i in range(0,13):
            for j in range(0, 13):
                prime = Card.PRIMES[i] * Card.PRIMES[j]
                cs = Card.STR_RANKS[i] + Card.STR_RANKS[j]
                prime_map[prime] = cs
        for i in sorted_items:
            p = i[0]
            v = i[1]
            s = ""
            if p > 10000:
                cs = prime_map[p-10000]
                s = "o"
                res += "%s%s  %s\n" % (cs, s, v)
            else:
                cs = prime_map[p]
                s = "s"
                res += "%s%s  %s\n" % (cs,s,v)
        fn = "%s/handsta_%s_%s.txt" % (shark.game_config.gg.data_dir_path,self.name,self.count)
        f = file(fn,"w")
        f.write(res)
        f.close()

    def hand_card_product(self):
        h1_suit = Card.get_suit_int(self.hand_card[0])
        h2_suit = Card.get_suit_int(self.hand_card[1])
        if h1_suit == h2_suit:
            return Card.prime_product_from_hand(self.hand_card)
        else:
            return Card.prime_product_from_hand(self.hand_card) + 10000

    def hand_card_product_value(self):
        return self.hand_card_record[self.hand_card_product()] if self.hand_card_product() in self.hand_card_record else 100

    def flop(self, cards):
        self.board.extend(cards)

    def turn(self, card):
        self.board.append(card)

    def river(self, card):
        self.board.append(card)
    
    def action(self, options , info):
        if info.round_name != ROUND_STATE_PRE:
            value = self.dealer.evaluate(self.hand_card,self.board)
            if value <= 1599:
                return PLAYER_ACTION_TYPE_ALLIN,options[PLAYER_ACTION_TYPE_ALLIN]
            elif value <= 6185:
                if PLAYER_ACTION_TYPE_CHECK in options:
                    return PLAYER_ACTION_TYPE_CHECK,options[PLAYER_ACTION_TYPE_CHECK]
                elif PLAYER_ACTION_TYPE_CALL in options:
                    return PLAYER_ACTION_TYPE_CALL, options[PLAYER_ACTION_TYPE_CALL]
                else:
                    return PLAYER_ACTION_TYPE_ALLIN,options[PLAYER_ACTION_TYPE_ALLIN]
            else:
                if PLAYER_ACTION_TYPE_CHECK in options:
                    return PLAYER_ACTION_TYPE_CHECK,options[PLAYER_ACTION_TYPE_CHECK]
                else:
                    return PLAYER_ACTION_TYPE_FOLD,0
        else:
            import random
            if random.randint(1,90) > self.hand_card_product_value():
                return PLAYER_ACTION_TYPE_FOLD,0
            else:
                if PLAYER_ACTION_TYPE_CALL in options:
                    return PLAYER_ACTION_TYPE_CALL,options[PLAYER_ACTION_TYPE_CALL]
                else:
                    return PLAYER_ACTION_TYPE_ALLIN, options[PLAYER_ACTION_TYPE_ALLIN]