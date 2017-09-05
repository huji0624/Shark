#!/usr/bin/python


GAME_MODEL_DEBUG = 0
GAME_MODEL_PROFILE = 1
GAME_MODEL_RELEASE = 2


GAME_LOG_LEVEL_DEBUG = 0
GAME_LOG_LEVEL_INFO = 1
GAME_LOG_LEVEL_ERR = 2
GAME_LOG_LEVEL_NO = 5


class GameConfig:
    def __init__(self, round_limit=-1, model=GAME_MODEL_RELEASE, log_level=GAME_LOG_LEVEL_ERR):
        self.round_limit = round_limit
        self.model = model
        self.log_level = log_level

    @property
    def is_debug_model(self):
        return self.model == GAME_MODEL_DEBUG

    @property
    def is_log_level_debug(self):
        return self.log_level == GAME_LOG_LEVEL_DEBUG


global_game_config = None
