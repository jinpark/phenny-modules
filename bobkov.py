# -*- coding: utf8 -*-
"""
markov.py - bob markov Module
"""

from sopel.module import commands, example
from markov-text.db import Db
from markov-text.gen import Generator
from markov-text.parse import Parser
from markov-text.sql import Sql
from markov-text.rnd import Rnd
import sys
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
