from sym_api_client_python.clients.sym_bot_client import APIClient
from sym_api_client_python.clients.user_client import UserClient
import codecs, json, os
import asyncio
import logging



class Filler():
    def __init__(self, bot_client):
        self.bot_client = bot_client

    async def filler(self, msg):
        display = "<card accent='tempo-bg-color--blue' iconSrc=''><body><h1>filler</h1></body></card>"
        self.bot_client.get_message_client().send_msg(msg['stream']['streamId'], dict(message="""<messageML>""" + display + """</messageML>"""))

## lalalal
class BotReader():
    def __init__(self, bot_client):
        self.bot_client = bot_client


    async def getList(self, msg):
        rsslist = self.bot_client.reader.get_list()
        display = "<card accent='tempo-bg-color--blue' iconSrc=''><body>"
        for i in rsslist:
            display += "<p>" + i + "</p>"
        display += "</body></card>"
        self.bot_client.get_message_client().send_msg(msg['stream']['streamId'], dict(message="""<messageML>""" + display + """</messageML>"""))
    
    async def checkNews(self, msg):
        display = "<card accent='tempo-bg-color--blue' iconSrc=''><body><ul><li>.</li>"
        feeds = self.bot_client.reader.checkrss()
        if len(feeds) == 0:
            display += "<li>No Feeds</li>"
        for topic in feeds:
            for feed in feeds[topic]:
                display += "<li><p><a href='" + feed['link'] + "'>" + feed['title'] + "</a></p></li>"
        display += "</ul></body></card>"
        self.bot_client.get_message_client().send_msg(msg['stream']['streamId'], dict(message="""<messageML>""" + display + """</messageML>"""))

    async def addRss(self, msg, name, url):
        # TODO: add try / catch
        if self.bot_client.reader.add_rss_item(name, url):
            display = "<card accent='tempo-bg-color--blue' iconSrc=''><body><p>Feed <b>" + name + " </b>" + " added</p></body></card>"
        else:
            display = "<card accent='tempo-bg-color--blue' iconSrc=''><body><p>Error</p></body></card>"

        self.bot_client.get_message_client().send_msg(msg['stream']['streamId'], dict(message="""<messageML>""" + display + """</messageML>"""))
            

    async def delRss(self, msg, name):
        if self.bot_client.reader.del_rss_item(name):
            display = "<card accent='tempo-bg-color--blue' iconSrc=''><body><p>Feed <b>" + name + " </b>" + " deleted</p></body></card>"
        else:
            display = "<card accent='tempo-bg-color--blue' iconSrc=''><body><p>Error</p></body></card>"

        self.bot_client.get_message_client().send_msg(msg['stream']['streamId'], dict(message="""<messageML>""" + display + """</messageML>"""))

        


