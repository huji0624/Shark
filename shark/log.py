#!/usr/bin/python


import game_config


def logD(msg):
    if game_config.global_game_config.log_level == game_config.GAME_LOG_LEVEL_DEBUG:
        print "[DEBUG]" + msg


def logI(msg):
    if game_config.global_game_config.log_level < game_config.GAME_LOG_LEVEL_ERR:
        print "[INFO]" + msg


def logE(msg):
    print "[ERR]" + msg
    import winsound
    winsound.Beep(600, 2000)
    exit(1)
