#!/usr/bin/python




from deuces import *
import random
from desk import *
import player_state
from polaris import *
import game_config
from dealer import *
import time
from result import *


class GameEngine:
    def __init__(self, game_config_):
        game_config.gg = game_config_
        self.roundCount = 1
        self.desk = Desk(DeskConfig(200, 2, 1))
        self.dealer = Dealer(self.desk)
        self.polaris = Polaris()
        self.start_time = 0

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
        self.start_time = time.time()

    def game_end(self):
        self.desk.end()
        dt = time.time() - self.start_time
        print "%s hands were played for one second." % (self.roundCount / dt)
        if game_config.gg.save_data_count_limit == -1:
            game_config.gg.hand_recorder.set_save_path(game_config.gg.recorder_path)
            game_config.gg.hand_recorder.save_to_file()
            self.polaris.plot_all()

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
        self.dealer.round_start()
        for p in self.desk.players:
            p.interface.dealer = self.dealer
            p.interface.desk_config = self.desk.config

    def check_round(self):
        if len(self.desk.players_not_state(player_state.PLAYER_STATE_FOLD)) == 1:
            return False
        else:
            return True

    def roundEnd(self):
        result = self.dealer.round_end()
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
        logD("deal + %s" % (self.dealer.deal_get_chips))
        total = 0
        for change in changes.values():
            total = total + change
        total = total + self.dealer.deal_get_chips
        if total != 0:
            logE("some thing wrong.total not 0.")
        result_dict = {}
        for k, v in result.items():
            result_dict[k] = v.chips_gain
        game_config.gg.hand_recorder.end_hand(result_dict)
        if game_config.gg.save_data_count_limit != -1:
            limit = game_config.gg.save_data_count_limit
            if self.roundCount % limit == 0:
                po_path = "%s/chips_%s.png" % (game_config.gg.data_dir_path, self.roundCount)
                self.polaris.plot_all(po_path)
                self.polaris = Polaris()
                re_path = "%s/record_%s.json" % (game_config.gg.data_dir_path, self.roundCount)
                game_config.gg.hand_recorder.set_save_path(re_path)
                game_config.gg.hand_recorder.save_to_file()

    def preFlop(self):
        logI("++pre flop++")
        pcount = len(self.desk.players)
        if pcount > 2:
            preactions = [SmallBlind(self.desk.player_at_position(0), self.desk.config.small_blind)]
            preactions.append(BigBlind(self.desk.player_at_position(1), self.desk.config.big_blind))
            self.dealer.new_bet_round("preflop", preactions)
            self.dealer.run_bet_round()
        else:
            logE("not enough player.game stopped.")

    def flop(self):
        logI("++flop++")
        self.desk.flop()
        self.dealer.new_bet_round("flop", None)
        self.dealer.run_bet_round()

    def turn(self):
        logI("++turn++")
        self.desk.turn()
        self.dealer.new_bet_round("turn", None)
        self.dealer.run_bet_round()

    def river(self):
        logI("++river++")
        self.desk.river()
        self.dealer.new_bet_round("river", None)
        self.dealer.run_bet_round()
