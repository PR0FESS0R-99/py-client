import requests
import json
from Telethroid.types import Msg
import pymongo

class Filter:
    def __init__(self):
        pass

    @staticmethod
    async def pvt(message):
        """Private message filter"""
        return message.chat.type == "private"

    @staticmethod
    async def gpt(message):
        """Group message filter"""
        return message.chat.type in ["group", "supergroup"]

    @staticmethod
    async def user(message, user_id):
        """User filter"""
        return message.from_user and message.from_user.id == user_id

    @staticmethod
    async def regex(message, pattern):
        """Regex filter"""
        return re.search(pattern, message.text)

    @staticmethod
    async def edited(message):
        """Edited message filter"""
        return message.edit_date is not None

    @staticmethod
    async def channel(message):
        """Channel message filter"""
        return message.chat.type == "channel"

    @staticmethod
    async def document(message):
        """Document filter"""
        return message.document

    @staticmethod
    async def voice(message):
        """Voice message filter"""
        return message.voice

    @staticmethod
    async def event(message, event_type):
        """Event filter"""
        return message.chat.type == "supergroup" and message.event and message.event.type == event_type

    @staticmethod
    async def photo(message):
        """Photo filter"""
        return message.photo

    @staticmethod
    async def sticker(message):
        """Sticker filter"""
        return message.sticker

    @staticmethod
    async def media(message):
        """Media filter"""
        return message.media_group_id is not None or message.photo or message.video or message.document or message.audio or message.voice or message.sticker or message.animation

    @staticmethod
    async def note(message):
        """Note filter"""
        return message.chat.type == "channel" and message.text is None and message.document is None and message.photo is None and message.voice is None

    @staticmethod
    async def poll(message):
        """Poll filter"""
        return message.poll

    @staticmethod
    async def anonymous(message):
        """Anonymous filter"""
        return message.chat.type == "supergroup" and message.from_user is None

    @staticmethod
    async def quiz(message):
        """Quiz filter"""
        return message.quiz

    @staticmethod
    async def web_page(message):
        """Web page filter"""
        return message.text and any(url in message.text for url in ["http://", "https://"]) and message.entities and message.entities[0].type == "url"

    @staticmethod
    async def new_chat_members(message):
        """New chat members filter"""
        return message.new_chat_members

    @staticmethod
    async def left_chat_members(message):
        """Left chat members filter"""
        return message.left_chat_member

    @staticmethod
    async def clone(message):
        """Clone filter"""
        return message.forward_from_chat or message.forward_from_message_id or message.forward_sender_name

    @staticmethod
    async def pymongo(message, db, collection):
        """PyMongo filter"""
        if db and collection:
            client = pymongo.MongoClient()
            db = client[db]
            collection = db[collection]
            return collection.find_one({"_id": message.chat.id}) is not None
        else:
            raise ValueError("Please provide the database and collection names")

    @staticmethod
    async def chat_title(message, title):
        """Chat title filter"""
        return message.chat.title == title

    @staticmethod
    async def get_chat_members(message):
        """Get chat members filter"""
        chat_members = await message.chat.get_members()
        return chat_members

    @staticmethod
    def delete_chat_title(message):
        """Filters updates where the chat's title has been deleted."""
        return message.chat and not message.chat.title

    @staticmethod
    def chat_photo(message):
        """Filters updates where a new chat photo has been set."""
        return message.chat and message.chat.photo

    @staticmethod
    def delete_chat_photo(message):
        """Filters updates where the chat photo has been deleted."""
        return message.chat and not message.chat.photo

    @staticmethod
    def forward(message):
        """Filters updates where a message has been forwarded."""
        return message.forward_date

    @staticmethod
    def supergroup(message):
        """Filters updates where the chat is a supergroup."""
        return message.chat and message.chat.type == 'supergroup'

    @staticmethod
    def delete_group(message):
        """Filters updates where a group has been deleted."""
        return message.chat and message.chat.type == 'group' and message.delete_chat_photo

    @staticmethod
    def delete_channel(message):
        """Filters updates where a channel has been deleted."""
        return message.chat and message.chat.type == 'channel' and message.delete_chat_photo

    @staticmethod
    def command(cmd: str, prefix: str = '/') -> bool:
        def func(message: dict) -> bool:
            if 'text' not in message:
                return False
            text = message['text'].strip()
            if not text.startswith(prefix):
                return False
            parts = text.split(' ')
            if len(parts) == 0:
                return False
            return parts[0][len(prefix):] == cmd
        return func

