import argparse
import asyncio
import logging
import os, sys, codecs, json

from sym_api_client_python.auth.auth import Auth
from sym_api_client_python.auth.rsa_auth import SymBotRSAAuth
from sym_api_client_python.clients.sym_bot_client import SymBotClient
from sym_api_client_python.configure.configure import SymConfig
from listeners.im_listener_imp import AsyncIMListenerImp
from listeners.room_listener_imp import AsyncRoomListenerImp
from rssreader import RssReader as reader

## Loading config json files
_configPath = os.path.abspath('../resources/config.json')
with codecs.open(_configPath, 'r', 'utf-8') as json_file:
        _config = json.load(json_file)


def configure_logging():
        logging.basicConfig(
                stream=sys.stdout,
                format='%(asctime)s - %(levelname)s - %(message)s',
                filemode='w', level=logging.INFO
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
        mr = reader.RssReader('../resources/state.json')
        bot_client.reader = mr

        # Initialize datafeed service
        datafeed_event_service = bot_client.get_async_datafeed_event_service()

        # Initialize listener objects and append them to datafeed_event_service
        # Datafeed_event_service polls the datafeed and the event listeners
        # respond to the respective types of events
        im_listener = AsyncIMListenerImp(bot_client)
        datafeed_event_service.add_im_listener(im_listener)

        room_listener = AsyncRoomListenerImp(bot_client)
        datafeed_event_service.add_room_listener(room_listener)

        # Create and read the datafeed
        logging.info('Datafeed started - bot is ready')
        loop = asyncio.get_event_loop()
        awaitables = asyncio.gather(datafeed_event_service.start_datafeed())
        loop.run_until_complete(awaitables)

if __name__ == "__main__":
    main()
 
