import argparse
import asyncio
import logging
import os, sys, codecs, json
import time

from sym_api_client_python.auth.auth import Auth
from sym_api_client_python.auth.rsa_auth import SymBotRSAAuth
from sym_api_client_python.clients.sym_bot_client import SymBotClient
from sym_api_client_python.configure.configure import SymConfig
from rssreader import RssReader as reader

## Loading config json files
_configPath = os.path.abspath('../resources/config.json')
with codecs.open(_configPath, 'r', 'utf-8') as json_file:
        _config = json.load(json_file)


def configure_logging():
        level_str = _config['log_level']
        m_level = logging.INFO
        if level_str == '': m_level = logging.NOTSET
        elif level_str == 'DEBUG': m_level = logging.DEBUG
        elif level_str == 'INFO': m_level = logging.INFO
        elif level_str == 'WARNING': m_level = logging.WARNING
        elif level_str == 'ERROR': m_level = logging.ERROR
        elif level_str == 'CRITICAL': m_level = logging.CRITICAL
        else: 
                print("Invalid log level")
                quit()

        logging.basicConfig(
                stream=sys.stdout,
                format='%(asctime)s - %(levelname)s - %(message)s',
                filemode='w', level=m_level
        )


loopCount = 0
def main():
        global loopCount

        # Configure log
        configure_logging()

        # Cert Auth flow: pass path to certificate config.json file
        
        config_path = os.path.join(os.path.dirname(__file__), "../resources", "config.json")
        
        configure = SymConfig(config_path, config_path)
        configure.load_config()

        auth = SymBotRSAAuth(configure)
        auth.authenticate()

        # Initialize SymBotClient with auth and configure objects
        bot_client = SymBotClient(auth, configure)

        # add rss instance to bot
        
        #bot_client.reader = mr

        stream = 'JjRqq6OBIa7s5wkdNI1b8n___otjgHfIdA'
        
        count = 0
        while True:
                logging.debug('XXXX Loop stream ' + stream)
                count = count + 1
                display = "<card accent='tempo-bg-color--blue' iconSrc=''><body><h1>LOOP: " + str(count) + "</h1></body></card>"
                bot_client.get_message_client().send_msg(stream, dict(message="""<messageML>""" + display + """</messageML>"""))
                time.sleep(3)
                display = "<card accent='tempo-bg-color--blue' iconSrc=''><body>"
                mr = reader.RssReader('../resources/state.json')
                feeds = mr.checkrss()
                if len(feeds) == 0:
                        display += "No Feeds"
                for topic in feeds:
                        for feed in feeds[topic]:
                                logging.debug('adding feeed to show')
                                display += "<p><a href='" + feed['link'] + "'>" + feed['title'] + "</a></p>"
                display += "</body></card>"
                print(display)
                bot_client.get_message_client().send_msg(stream, dict(message="""<messageML>""" + display + """</messageML>"""))


if __name__ == "__main__":
    main()
 