from sym_api_client_python.clients.user_client import UserClient
from commands.command import Filler, BotReader
import logging
import codecs
import json
import os


class MessageProcessor:

    def __init__(self, bot_client):
        self.bot_client = bot_client
    
    async def processor(self, msg):
        ## Normal message in the chat - no @mention of #hashtag nor $cashtag
        msg_xml = msg['message']
        
        me = "@spaceinvader"
        message_raw = self.sym_message_parser.get_text(msg)
        if me not in msg_xml:
            print("Not mentioned")
            return
        
        cmd = ''
        cmd_idx = 0
        for i in range(len(message_raw)):
            if message_raw[i] == me:
                cmd = message_raw[i+1]
                cmd_idx = i
        print("CMD: " + cmd)

        if cmd == '/add':
            print("ADD CMD")
            name = message_raw[cmd_idx + 2]
            url = message_raw[cmd_idx + 3]
            return await BotReader.addRss(self, msg, name, url)

        if cmd == '/del':
            print("DEL CMD")
            name = message_raw[cmd_idx + 2]
            return await BotReader.delRss(self, msg, name)

        if cmd == '/list':
            print("LIST CMD")
            return await BotReader.getList(self, msg)

        if cmd == '/check':
            print("CHECK CMD")
            return await BotReader.checkNews(self, msg)
        
 