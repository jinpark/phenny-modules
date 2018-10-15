
# -*- coding: utf8 -*-
"""
jisho.py - Willie giphy Module
"""

from sopel.module import commands, example
import requests

JISHO_API = "https://jisho.org/api/v1/search/words?keyword={}"

@commands('jisho')
@example('.jisho cat')
def jisho(bot, trigger):
    """.giphy cat"""
    API_KEY = bot.config.apikeys.giphy
    user_input = trigger.group(2)
    r = requests.get(JISHO_API.format(user_input))
    jisho_data = r.json()
    if len(jisho_data['data']) > 0:
        data = jisho_data['data'][0]
        response_string = u""
        if "word" in data["japanese"][0]:
            response_string += (u"Japanese Word: {j_word}, ".format(data["japanese"][0]["word"]))
        
        
        response_string += u"japanese reading {j_reading}. English Definition 1. {e_def}".format(
            j_reading=data["japanese"][0]["reading"],
            e_def=data["senses"][0]["english_definitions"][0]
        )
        bot.say(response_string)
    else:
        bot.say('No jisho data found. Blame bob')