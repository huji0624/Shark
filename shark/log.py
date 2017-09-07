#!/usr/bin/python


import game_config


def logD(msg):
    if game_config.gg.log_level == game_config.GAME_LOG_LEVEL_DEBUG:
        print "[DEBUG]" + msg


def logI(msg):
    if game_config.gg.log_level < game_config.GAME_LOG_LEVEL_WARNING:
        print "[INFO]" + msg


def logW(msg):
    if game_config.gg.log_level < game_config.GAME_LOG_LEVEL_ERR:
        print "[WARNING]" + msg

def logE(msg):
    print "[ERR]" + msg
    if game_config.gg.is_debug_model:
        import winsound
        winsound.Beep(600, 2000)
    exit(1)
