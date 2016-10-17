#!/usr/bin/python
# -*- coding: utf8 -*-

TOKEN = '279157398:AAHfF2Kcd_t-3VMUoYHvT236HzFpo1xoDqc'


import sys
import random
import telepot
import telepot.helper
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.delegate import (
    per_chat_id, per_callback_query_origin, create_open, pave_event_space)

"""
$ python3.5 quiz.py <token>
Send a chat message to the bot. It will give you a math quiz. Stay silent for
10 seconds to end the quiz.
It handles callback query by their origins. All callback query originated from
the same chat message will be handled by the same `CallbackQueryOriginHandler`.
"""

class QuizStarter(telepot.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(QuizStarter, self).__init__(*args, **kwargs)

    def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        self.sender.sendMessage(
            'Press START to do some math ...',
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[
                    InlineKeyboardButton(text='START', callback_data='start'),
                ]]
            )
        )
        self.close()  # let Quizzer take over

class Quizzer(telepot.helper.CallbackQueryOriginHandler):
    def __init__(self, *args, **kwargs):
        super(Quizzer, self).__init__(*args, **kwargs)
        self._score = {True: 0, False: 0}
        self._answer = None

    def _show_next_question(self):
        x = random.randint(1,50)
        y = random.randint(1,50)
        sign, op = random.choice([('+', lambda a,b: a+b),
                                  ('-', lambda a,b: a-b),
                                  ('x', lambda a,b: a*b)])
        answer = op(x,y)
        question = '%d %s %d = ?' % (x, sign, y)
        choices = sorted(list(map(random.randint, [-49]*4, [2500]*4)) + [answer])

        self.editor.editMessageText(question,
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    list(map(lambda c: InlineKeyboardButton(text=str(c), callback_data=str(c)), choices))
                ]
            )
        )
        return answer

    def on_callback_query(self, msg):
        query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')

        if query_data != 'start':
            self._score[self._answer == int(query_data)] += 1

        self._answer = self._show_next_question()

    def on__idle(self, event):
        text = '%d out of %d' % (self._score[True], self._score[True]+self._score[False])
        self.editor.editMessageText(text, reply_markup=None)
        self.close()




bot = telepot.DelegatorBot(TOKEN, [
    pave_event_space()(
        per_chat_id(), create_open, QuizStarter, timeout=3),
    pave_event_space()(
        per_callback_query_origin(), create_open, Quizzer, timeout=10),
])

bot.message_loop(run_forever='Listening ...')




import sys
import time
import random
import telepot
import time
import calendar
import urllib2
import xml.etree.ElementTree as ET

"""
$ python2.7 skeleton.py <token>
A skeleton for your telepot programs.
"""

def SendRandomMsg(chat_id, msg_list):
    bot.sendMessage(chat_id, msg_list[random.randint(0, len(msg_list)-1)])


def handle(msg):
    if start:
        flavor = telepot.flavor(msg)
        print flavor

        # a normal message
        if flavor == 'normal':
            content_type, chat_type, chat_id = telepot.glance2(msg)
            print content_type, chat_type, chat_id

            if content_type == 'text':
                command = msg['text']

                print 'Got message: %s' % command

                if 'sergio'.lower() in command.lower():
                    text = [
                            u'Ho sempre sostenuto che Sergio è un pirla',
                            u'Sergio?? ma chi?? quello pelato??',
                            u'Sergio è un coglione....Sergio è un coglione...',
                            u'Lo sapete che Sergio si trastulla con Parisotto?',
                            u'Sergio è un mio amico intimo!',
                            u'Attenzione...probabile BOMBA D\'ACQUA, Sergio confermi?'
                            ]
                    SendRandomMsg(chat_id, text)

                elif ('buongiorno'.lower() in command.lower()) or ('ciao'.lower() in command.lower()):
                    text = [
                            u'Buongiono a voi fighette!',
                            u'Si si...scrivete il buongiorno solo per vedere una figa!',
                            u'Dai testine, credete sia una bella giornata? invece no! solo bombe d\'acqua!',
                            u'Ciao cari!',
                            u'Ciao testa di cazzo!',
                            ]
                    SendRandomMsg(chat_id, text)

                elif (('mostra'.lower() in command.lower()) or ('manda'.lower() in command.lower())) \
                        and ('foto'.lower() in command.lower()) and ('tua'.lower() in command.lower()):
                    pics = [
                        'IMG-20160119-WA0008.jpg',
                        'IMG-20160119-WA0009.jpg',
                        'IMG-20160119-WA0010.jpg',
                    ]
                    filename = 'pics/'
                    filename += pics[random.randint(0, len(pics)-1)]
                    response = bot.sendPhoto(chat_id, open(filename, 'rb'))
                    print response

                elif ('silvio'.lower() in command.lower()) and ('ore'.lower() in command.lower()):
                    localtime = time.asctime( time.localtime(time.time()))
                    text = [
                            u'Guarda l\'orologio coglione!',
                            u'L\'ora di ieri a quest\'ora, pirla! ahahah',
                            u'Sei sicuro di volerlo sapere? ' + str(localtime),
                            u'...è l\'ora che ti svegli!',
                            u'eh sì ciao...mica go l\'orologio! chiedi a Sergio!',
                            u'uffa...la gheto finia de disturbarme par ste troiade?',
                            u'Vabbeh sono ' + str(time.time()) + u' secondi dal mezzanotte del primo gennaio del 1970',
                            ]
                    SendRandomMsg(chat_id, text)

                elif ('silvio'.lower() in command.lower()) and ('meteo'.lower() in command.lower()):
                    text = [
                            u'Guarda in questo gruppo ci sono persone che non capiscono un cazzo di meteo...!',
                            u'Allarme bomba d\'acqua',
                            u'Vai sul forum di Sergio!',
                            u'Previsioni di stocazzo! Qui pove sempre',
                            u'L\'è bel',
                            u'Sì ciao, e lo chiedi a me?',
                            u'Ma che cazzo è il meteo? l\'abbreviazione dei miei meteorismi?',
                            u'Tornado glaciale!',
                            ]
                    SendRandomMsg(chat_id, text)

                elif ('accend'.lower() in command.lower()) and ('luc'.lower() in command.lower()):
                    text = [
                            u'Impisa la lampadina!',
                            u'Taca tutto!',
                            u'Click!',
                            ]
                    SendRandomMsg(chat_id, text)

                elif ('spegn'.lower() in command.lower()) and ('luc'.lower() in command.lower()):
                    text = [
                            u'Stua la lampadina!',
                            u'Staca tutto!',
                            u'Click!',
                            ]
                    SendRandomMsg(chat_id, text)

                elif 'git'.lower() in command.lower():
                    text = [
                            u'Ma usa SVN cazzo!',
                            u'GIT il programma più difficile da configurare...',
                            u'Va in figa GIT!',
                            u'Te ga dito nessuno che GIT xe na merda?',
                            ]
                    SendRandomMsg(chat_id, text)

                elif (('euro'.lower() in command.lower()) and ('dollaro'.lower() in command.lower())) or \
                        (('eur'.lower() in command.lower()) and ('usd'.lower() in command.lower())):
                    response = urllib2.urlopen('http://www.ecb.int/stats/eurofxref/eurofxref-daily.xml')
                    xml = response.read()
                    root = ET.fromstring(xml)
                    eurusd = root.find("./{http://www.ecb.int/vocabulary/2002-08-01/eurofxref}Cube/{http://www.ecb.int/vocabulary/2002-08-01/eurofxref}Cube/{http://www.ecb.int/vocabulary/2002-08-01/eurofxref}Cube[@currency='USD']")
                    tasso_di_cambio = eurusd.attrib["rate"]

                    text = [
                            u'EUR-USD: %s! sono efficiente, no?' % str(tasso_di_cambio),
                            u'Chiedi a Nemo!',
                            u'Compra dollari, vecio!!',
                            u'%s! Borse del cavolo' % str(tasso_di_cambio),
                            ]
                    SendRandomMsg(chat_id, text)




# Query inline
from telepot.delegate import per_inline_from_id, create_open, pave_event_space

class InlineHandler(telepot.helper.InlineUserHandler, telepot.helper.AnswererMixin):
    def __init__(self, *args, **kwargs):
        super(InlineHandler, self).__init__(*args, **kwargs)

    def on_inline_query(self, msg):
        def compute_answer():
            query_id, from_id, query_string = telepot.glance(msg, flavor='inline_query')
            print(self.id, ':', 'Inline Query:', query_id, from_id, query_string)

            articles = [{'type': 'article',
                             'id': 'abc', 'title': query_string, 'message_text': query_string}]

            return articles

        self.answerer.answer(msg, compute_answer)

    def on_chosen_inline_result(self, msg):
        from pprint import pprint
        pprint(msg)
        result_id, from_id, query_string = telepot.glance(msg, flavor='chosen_inline_result')
        print(self.id, ':', 'Chosen Inline Result:', result_id, from_id, query_string)




# creazione bot
bot = telepot.Bot(TOKEN)
start = False



bot = telepot.DelegatorBot(TOKEN, [
    pave_event_space()(
        per_inline_from_id(), create_open, InlineHandler, timeout=10),
])
bot.message_loop(run_forever='Listening ...')


# pulizia precedenti messagi non letti
msgs = bot.getUpdates()
if msgs:
    last_msg = msgs[-1]
    offset = last_msg["update_id"]
    start = True
    msgs = bot.getUpdates(offset=offset+1)

io = bot.getMe()
print ("Avvio il bot \"%s\"" % io["first_name"])
print ("In ascolto ...")

# aggancio handler per ricezione nuovi messaggi
bot.notifyOnMessage(handle)

# Keep the program running.
while 1:
    time.sleep(10)
