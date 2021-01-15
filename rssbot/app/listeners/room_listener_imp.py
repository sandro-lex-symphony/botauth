from .processors.room_processor import AsyncRoomProcessor
from sym_api_client_python.listeners.room_listener import RoomListener
import logging


class AsyncRoomListenerImp(RoomListener):
    def __init__(self, sym_bot_client):
        self.bot_client = sym_bot_client
        # self.message_parser = SymMessageParser()
        self.room_processor = AsyncRoomProcessor(self.bot_client)

    async def on_room_msg(self, msg):
        logging.debug('room msg received', msg)
        msg_processor = AsyncRoomProcessor(self.bot_client)
        await msg_processor.process(msg)

    async def on_room_created(self, room_created):
        logging.debug('room created', room_created)

    async def on_room_deactivated(self, room_deactivated):
        logging.debug('room Deactivated', room_deactivated)

    async def on_room_member_demoted_from_owner(self,
                                                room_member_demoted_from_owner):
        logging.debug('room member demoted from owner',
                      room_member_demoted_from_owner)

    async def on_room_member_promoted_to_owner(self, room_member_promoted_to_owner):
        logging.debug('room member promoted to owner',
                      room_member_promoted_to_owner)

    async def on_room_reactivated(self, room_reactivated):
        logging.debug('room reactivated', room_reactivated)

    async def on_room_updated(self, room_updated):
        logging.debug('room updated', room_updated)

    async def on_user_joined_room(self, user_joined_room):
        logging.debug('USER JOINED ROOM', user_joined_room)

    async def on_user_left_room(self, user_left_room):
        logging.debug('USER LEFT ROOM', user_left_room)