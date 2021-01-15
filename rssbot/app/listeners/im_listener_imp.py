from sym_api_client_python.listeners.im_listener import IMListener
from .processors.im_processor import AsyncIMProcessor
import logging


class AsyncIMListenerImp(IMListener):
    """Example implementation of IMListener with asynchronous functionality
    Call the bot with /wait to see an example of a non-blocking wait
    """

    def __init__(self, sym_bot_client):
        self.bot_client = sym_bot_client
        self.im_processor = AsyncIMProcessor(self.bot_client)

    async def on_im_message(self, msg):
        logging.debug('message received in IM', msg)
        await self.im_processor.process(msg)

    async def on_im_created(self, im_created):
        logging.debug("IM created!", im_created)