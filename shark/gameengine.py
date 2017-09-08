#!/usr/bin/python




from deuces import *
import random
import betround
from log import *
from pot import *
from desk import *
import player_state
from polaris import *
import game_config
from dealer import *


class Result:
    def __init__(self, chips, hand_card, position):
        self.chips_gain = chips
        self.hand_card = hand_card
        self.position = position

    def __str__(self):
        return "chips + %s;" % self.chips_gain

    __repr__ = __str__


class GameEngine:
    def __init__(self, game_config_):
        game_config.gg = game_config_
        self.roundCount = 1
        self.desk = Desk(DeskConfig(200, 2, 1))
        self.pot = None
        self.dealer = Dealer()
        self.deal_get_chips = 0
        self.polaris = Polaris()

    def start(self):
        if game_config.gg.model == game_config.GAME_MODEL_PROFILE:
            import profile
            profile.run("self.start_()")
        else:
            self.start_()

    def start_(self):
        self.game_start()
        while 1:
            self.roundStart()
            self.preFlop()
            if self.check_round():
                self.flop()
                if self.check_round():
                    self.turn()
                    if self.check_round():
                        self.river()
            self.roundEnd()
            if self.roundCount == game_config.gg.round_limit:
                logI("stop game because round limit.")
                break
        self.game_end()

    def game_start(self):
        self.desk.start()

    def game_end(self):
        self.desk.end()
        if game_config.gg.model == game_config.GAME_MODEL_DEBUG:
            game_config.gg.hand_recorder.set_save_file(game_config.gg.recorder_path)
            game_config.gg.hand_recorder.save_to_file()
            self.polaris.show()

    def addPlayer(self, player):
        if player.name is None:
            print "add player fail.name must be set."
            return
        self.desk.add_player(player)

    def roundStart(self):
        print "----round %d start----" % (self.roundCount)
        game_config.gg.hand_recorder.new_hand(self.roundCount)
        self.roundCount = self.roundCount + 1
        self.desk.round_start()
        self.pot = Pot()
        for p in self.desk.players:
            p.interface.dealer = self.dealer
            p.interface.desk_config = self.desk.config

    def check_round(self):
        if len(self.desk.players_not_state(player_state.PLAYER_STATE_FOLD)) == 1:
            return False
        else:
            return True

    def roundEnd(self):
        result = None
        not_fold_players = self.desk.players_not_state(player_state.PLAYER_STATE_FOLD)
        if len(not_fold_players) > 1:
            result = self.show_hand(not_fold_players)
        elif len(not_fold_players) == 1:
            result = self.win(not_fold_players[0])
        else:
            logE("this can not happen.")
        self.desk.round_end(result)
        changes = {}
        for p in self.desk.players:
            if game_config.gg.chips_model == game_config.GAME_CHIPS_MODEL_CUM:
                if p.chips == 0:
                    p.chips = self.desk.config.buy_in
                    p.chips_gain = p.chips_gain - self.desk.config.buy_in
            else:
                dc = p.chips - self.desk.config.buy_in
                p.chips = self.desk.config.buy_in
                p.chips_gain = p.chips_gain + dc
            chips_change = p.chips - self.desk.config.buy_in + p.chips_gain
            changes[p.name] = chips_change
            self.polaris.mark_chips_change(p.name, chips_change, self.roundCount)
            logD("Player %s %s" % (p.name, chips_change))
        logD("deal + %s" % (self.deal_get_chips))
        total = 0
        for change in changes.values():
            total = total + change
        total = total + self.deal_get_chips
        if total != 0:
            logE("some thing wrong.total not 0.")
        result_dict = {}
        for k,v in result.items():
            result_dict[k] = v.chips_gain
        game_config.gg.hand_recorder.end_hand(result_dict)
        if game_config.gg.model == game_config.GAME_MODEL_RELEASE:
            limit = game_config.gg.save_data_count_limit
            if self.roundCount % limit  == 0:
                po_path = "%s/%s.png" % (game_config.gg.dir_path,self.roundCount)
                self.polaris.show(po_path)
                self.polaris = Polaris()
                re_path = "%s/%s.json" % (game_config.gg.dir_path,self.roundCount)
                game_config.gg.hand_recorder.set_save_path(re_path)
                game_config.gg.hand_recorder.save_to_file()


    def show_hand(self, not_fold_players):
        result = {}
        chips_gain_map = dict()
        for player in not_fold_players:
            chips_gain_map[player.name] = 0
            player.hand_value = self.dealer.evaluate(player.hand_card, self.desk.board)
        for round_pot_ in self.pot.round_pots:
            if round_pot_.has_side_pot():
                for side_pot in round_pot_.side_pots:
                    self.show_hand_in_pot(side_pot.chips, side_pot.players, chips_gain_map)
            else:
                self.show_hand_in_pot(round_pot_.chips, not_fold_players, chips_gain_map)
        for key, value in chips_gain_map.items():
            player = self.desk.player_with_name(key)
            result[key] = Result(value, player.hand_card, self.desk.players.index(player))
        logD("Result for round:======\n %s" % (result))
        return result

    def show_hand_in_pot(self, chips, players, chips_gain_map):
        tmp_players = []
        for p in players:
            if p.state != player_state.PLAYER_STATE_FOLD:
                tmp_players.append(p)
        players = tmp_players
        sorted_players = sorted(players, key=lambda player: player.hand_value)
        logD("show hand in round pot %s with player %s" % (chips, sorted_players))
        top_value_players = [sorted_players.pop(0)]
        for player in sorted_players:
            if player.hand_value == top_value_players[0].hand_value:
                top_value_players.append(player)
        top_count = len(top_value_players)
        chips = chips
        left = chips % top_count
        chips = chips - left
        each = chips / top_count
        self.deal_get_chips = self.deal_get_chips + left
        for player in top_value_players:
            player.chips = player.chips + each
            chips_gain_map[player.name] = chips_gain_map[player.name] + each

    def win(self, player):
        result = {}
        if player is None:
            logE("win player is None.")
        player.chips = player.chips + self.pot.chips
        result[player.name] = Result(self.pot.chips, None, self.desk.players.index(player))
        return result

    def preFlop(self):
        logI("++pre flop++")
        pcount = len(self.desk.players)
        if pcount > 2:
            br = betround.Betround(self.pot, self.desk, self.dealer)
            br.addPreBet(self.desk.config.small_blind)
            br.addPreBet(self.desk.config.big_blind)
            br.loop()
        else:
            logE("not enough player.game stopped.")

    def flop(self):
        logI("++flop++")
        self.desk.flop()
        betround.Betround(self.pot, self.desk, self.dealer).loop()

    def turn(self):
        logI("++turn++")
        self.desk.turn()
        betround.Betround(self.pot, self.desk, self.dealer).loop()

    def river(self):
        logI("++river++")
        self.desk.river()
        betround.Betround(self.pot, self.desk, self.dealer).loop()