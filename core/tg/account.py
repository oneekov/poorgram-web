from telethon import TelegramClient
from telethon.types import User
from telethon.sessions import StringSession
from telethon.errors import *
from .config import app_hash, app_id

#FIXME: Убрать это, оно было нужно только для теста
async def getUsername(session): #Temporary. Will be removed after tests
    client = TelegramClient(StringSession(session), app_id, app_hash)
    await client.connect()

    me = await client.get_me()
    username = me.username
    await client.disconnect()
    return username