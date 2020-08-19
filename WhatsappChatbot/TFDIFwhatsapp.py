from flask import Flask, request
from WhatsappChatbot.TFIDF.Transformer import Transformer
from twilio.twiml.messaging_response import MessagingResponse
from langdetect import detect
import pymongo
import os
from pymongo import MongoClient
import datetime

app = Flask(__name__)
transformer = Transformer('WhatsappChatbot/data/train/QnA.csv', 'WhatsappChatbot/data/train/SimplifiedChineseQnA.csv',
                          'WhatsappChatbot/data/train/traditionalChineseQnA.csv', 'WhatsappChatbot/data/train/SpanishQnA.csv')

MONGO_URI = os.environ['MONGO_URI']
cluster = MongoClient(MONGO_URI)
db = cluster["QandA"]
collection = db["QandA"]

numbers = []
greetings = {'en': 'Hello! Nice to meet you!', 'es':'¡Mucho gusto! ¿Cómo estás?', 'zh-cn':'您好！很高兴为您服务'}
passings = {'en': 'Sorry, I did not understand your question. ',
            'es': 'Lo siento, no entiendo su pregunta', 'zh-cn': '对不起，我没有理解您的问题'}

@app.route('/', methods=['POST'])
def bot():

    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    responded = False

    number = request.values.get('From', '')
    if not (incoming_msg == None or incoming_msg == ''):
        response, similarity = transformer.match_query(incoming_msg)
        re = ''
        # signifies first message in a conversation
        if not number in numbers and similarity < 0.5:
            language = detect(incoming_msg)
            if language in greetings.keys():
                re = greetings.get(language)
            else:
                re = re + greetings.get('en')
            msg.body(re)
            numbers.append(number)
            insert(incoming_msg, re, number)
            responded = True
        if not responded:
            if similarity < 0.5:
                language = detect(incoming_msg)
                if language in passings.keys():
                    re = passings.get(language)
                else:
                    re = passings.get('en')
                msg.body(re)
                insert(incoming_msg, re, number)
            else:
                responses = response.split('|')
                re = ''
                for r in responses:
                    if r != '':
                        re = re + '\n' + r.strip()
                msg.body(re)
                insert(incoming_msg, re, number)
            responded = True

    if not responded:
        msg.body('Sorry, I cannot understand your message')
    return str(resp)

def insert(message, response, recipient):
    time = datetime.datetime.now()
    collection.insert_one({"question": message, "answer": response, 'recipient': recipient,
                           'time': time, 'source': "Whatsapp"})
if __name__ == '__main__':
    app.run()

