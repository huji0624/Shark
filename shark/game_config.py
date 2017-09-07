#!/usr/bin/python


from hands_recorder import *

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
    def __init__(self, round_limit=-1, model=GAME_MODEL_RELEASE, log_level=GAME_LOG_LEVEL_ERR,
                 recorder_path="./hand_record.json", chips_model=GAME_CHIPS_MODEL_CUM):
        self.round_limit = round_limit
        self.model = model
        self.log_level = log_level
        self.hands_recorder = HandsRecorder(recorder_path)
        self.chips_model = chips_model

    @property
    def is_debug_model(self):
        return self.model == GAME_MODEL_DEBUG

    @property
    def is_log_level_debug(self):
        return self.log_level == GAME_LOG_LEVEL_DEBUG

    @property
    def hand_recorder(self):
        return self.hands_recorder


gg = None
