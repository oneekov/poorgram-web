from telethon import TelegramClient
from telethon.types import User
from telethon.sessions import StringSession
from telethon.errors import *
from .config import app_hash, app_id

async def getChats():
    return 0