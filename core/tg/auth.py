from telethon import TelegramClient
from telethon.types import User
from telethon.sessions import StringSession
from telethon.errors import *
from .config import app_hash, app_id

#FIXME: Добавить сюда обработку ошибок (в случаях, когда номер не указан верно, например)
#TODO: Сделать поддержку прокси. Лучше начать делать сейчас понемногу, чем через некоторое время переписывать для этого весь проект.

async def send_code(phone):
    client = TelegramClient(StringSession(), app_id, app_hash)
    await client.connect()
    login_token = await client.send_code_request(phone)
    await client.disconnect()
    return login_token.phone_code_hash, client.session.save()

async def tg_sign_in(session, phone=None, code=None, phone_hash=None, password=None):
    print(session)
    client = TelegramClient(StringSession(session), app_id, app_hash)
    await client.connect()
    try:
        if password==None: await client.sign_in(phone=phone, code=code, phone_code_hash=phone_hash, password=password)
        else: await client.sign_in(password=password)
        await client.disconnect()
        return True
    except SessionPasswordNeededError:
        await client.disconnect()
        return False
    except Exception as e:
        print(e)