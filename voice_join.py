
# -*- coding: utf8 -*-
"""
voide_join.py - Willie giphy Module
"""

from sopel.module import commands, rule, event
import threading

def give_voice(bot, trigger, username):
    channel = trigger.sender
    print(['give voice ran with', channel, username])
    return bot.write(['MODE', channel, '+v',username])

@event('JOIN')
@rule(r'.*')
def voice_join(bot, trigger):
    if  trigger.nick == bot.nick or trigger.isvoice:
        return
    timer = Threading.timer(30.0, give_voice, args=[bot, trigger, trigger.nick])
    
    