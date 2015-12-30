# -*- coding: utf8 -*-
"""
markov.py - bob markov Module
"""

from sopel.module import commands, example
import os
import sys
try:
    from markov_text.db import Db
    from markov_text.gen import Generator
    from markov_text.parse import Parser
    from markov_text.sql import Sql
    from markov_text.rnd import Rnd
except:
    sys.path.append(os.path.join(os.path.dirname(__file__), "markov_text"))
    from markov_text.db import Db
    from markov_text.gen import Generator
    from markov_text.parse import Parser
    from markov_text.sql import Sql
    from markov_text.rnd import Rnd
import sqlite3
import codecs

name = 'cbirkett'
WORD_SEPARATOR = ' '
db = Db(sqlite3.connect(name + '.db'), Sql())
generator = Generator(name, db, Rnd())

@commands('bobkov')
@example('.bobkov')
def bobkov(bot, trigger):
    """.bobkov - markov chain of bob"""
    bot.say(generator.generate(WORD_SEPARATOR))
