#!/usr/bin/python


from hands_recorder import *
import time
import os

GAME_MODEL_DEBUG = 0
GAME_MODEL_PROFILE = 1
GAME_MODEL_RELEASE = 2


GAME_LOG_LEVEL_DEBUG = 0
GAME_LOG_LEVEL_INFO = 1
GAME_LOG_LEVEL_WARNING = 2
GAME_LOG_LEVEL_ERR = 3
GAME_LOG_LEVEL_NO = 5



GAME_CHIPS_MODEL_CUM = 0
GAME_CHIPS_MODEL_CLEAR = 1


class GameConfig:
    def __init__(self, round_limit=-1,save_limit=10000, model=GAME_MODEL_RELEASE, log_level=GAME_LOG_LEVEL_ERR,
                 recorder_path="./hand_record.json", chips_model=GAME_CHIPS_MODEL_CUM):
        self.round_limit = round_limit
        self.model = model
        self.log_level = log_level
        self.recorder_path = recorder_path
        self.hands_recorder = HandsRecorder()
        self.chips_model = chips_model
        self.dir_path_var = os.path.split(os.path.realpath(__file__))[0] + time.strftime("/../datas/%Y-%m-%d_%H:%M:%S", time.localtime())
        self.save_data_count_limit = save_limit

    @property
    def is_debug_model(self):
        return self.model == GAME_MODEL_DEBUG

    @property
    def is_log_level_debug(self):
        return self.log_level == GAME_LOG_LEVEL_DEBUG

    @property
    def hand_recorder(self):
        return self.hands_recorder

    @property
    def dir_path(self):
        if not os.path.exists(self.dir_path_var):
            os.makedirs(self.dir_path_var)
        return self.dir_path_var

gg = None
