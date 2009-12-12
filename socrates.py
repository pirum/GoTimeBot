# Copyright (C) 2009 Go-time team
# For license information, see LICENSE.TXT

from twisted.words.protocols import irc
from twisted.internet import protocol
from twisted.internet import reactor

import sys
from collections import defaultdict
import random
import os
import re

markov = defaultdict(list)
STOP_WORD = "\n"


class SocratesBot(irc.IRCClient):
    def _get_nickname(self):
        return self.factory.nickname
    nickname = property(_get_nickname)

    def signedOn(self):
        self.join(self.factory.channel)
        print "Signed on as %s." % (self.nickname,)

    def joined(self, channel):
        print "Joined %s." % (channel,)

    def privmsg(self, user, channel, msg):
        if not user:
            return
        if self.nickname in msg:
            msg = re.compile(self.nickname + "[:,]* ?", re.I).sub('', msg)
            prefix = "%s: " % (user.split('!', 1)[0], )
        else:
            prefix = ''
            
        begins_with_nick = msg.startswith(self.nickname)
            
        add_to_brain(msg, self.factory.chain_length, write_to_file=True)
        if prefix or begins_with_nick or random.random() <= self.factory.chattiness:
            sentence = generate_sentence(msg, self.factory.chain_length,
                self.factory.max_words)
            if sentence:
                self.msg(self.factory.channel, prefix + sentence)



class SocratesBotFactory(protocol.ClientFactory):
    protocol = SocratesBot

    def __init__(self, channel, nickname, chain_length=2,
        chattiness=1.0, max_words=10000):
        self.channel = channel
        self.nickname = nickname
        self.chain_length = chain_length
        self.chattiness = chattiness
        self.max_words = max_words

    def clientConnectionLost(self, connector, reason):
        print "Lost connection (%s), reconnecting." % (reason,)
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "Could not connect: %s" % (reason,)


def add_to_brain(msg, chain_length, write_to_file=False):
    if write_to_file:
        f = open('training_text.txt', 'a')
        f.write(msg + '\n')
        f.close()
    buf = [STOP_WORD] * chain_length
    for word in msg.split():
        markov[tuple(buf)].append(word)
        del buf[0]
        buf.append(word)
    markov[tuple(buf)].append(STOP_WORD)


def generate_sentence(msg, chain_length, max_words=10000):
    buf = msg.split()[:chain_length]
    if len(msg.split()) > chain_length:
        message = buf[:]
    else:
        message = []
        for i in xrange(chain_length):
            message.append(random.choice(markov[random.choice(markov.keys())]))
    for i in xrange(max_words):
        try:
            next_word = random.choice(markov[tuple(buf)])
        except IndexError:
            continue
        if next_word == STOP_WORD:
            break
        message.append(next_word)
        del buf[0]
        buf.append(next_word)
    return ' '.join(message)



if __name__ == "__main__":

    chain_length = 2

    try:
        chan = sys.argv[1]
    except IndexError:
        print "Please specify a channel name."
        print "Example:"
        print "  python socrates.py go-time"
    if os.path.exists('training_text.txt'):
        f = open('training_text.txt', 'r')
        for line in f:
            add_to_brain(line, chain_length)
        print 'Brain Reloaded'
        f.close()
    reactor.connectTCP('irc.freenode.net', 6667, SocratesBotFactory('#' + chan,
        'Socrates98432', chain_length, chattiness=0.2))
    reactor.run()

