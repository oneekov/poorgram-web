from telethon import TelegramClient
from telethon.types import User
from telethon.sessions import StringSession
from telethon.errors import *
from .config import app_hash, app_id
import re

#TODO: Сделать поддержку прокси. Лучше начать делать сейчас понемногу, чем через некоторое время переписывать для этого весь проект.

'''
Функция принимает в качестве аргумента номер (в формате +XXXXXXXXXXX, тип str)
Затем отправляет запрос для кода (с помощью send_code_request)
И возвращает phone_code_hash (подробнее: https://core.telegram.org/constructor/auth.sentCode) и Auth Key

Если произошла ошибка, то возвращается 0 и осмысленную (или не совсем) ошибку

Обрабатываемые ошибки:
PhoneNumberInvalidError - неверный номер
FloodWaitError - грубо говоря, "повторите через X секунд"
'''
async def send_code(phone):
    client = TelegramClient(StringSession(), app_id, app_hash)
    await client.connect()

    try:
        login_token = await client.send_code_request(phone)
        await client.disconnect()
        return login_token.phone_code_hash, client.session.save()
    
    except PhoneNumberInvalidError: #Если номер неверный
        await client.disconnect()
        return 0, "Неверный номер"
    
    except FloodWaitError as e: #если Flood Wait
        await client.disconnect()
        return 0, f"Попробуйте через {re.search(r'\d+', str(e))[0]} секунд"

    except Exception as e: #Если что-то другое
        await client.disconnect()
        return 0, f"Uncaught error: {e}"



'''
Функция принимает в качестве аргументов сессию (Auth Key), номер, код для входа, phone_code_hash (см. функцию send_code) и пароль (опционально)

Если пароль не указан, то происходит попытка входа при помощи номера, кода и хеша
Если пароль указан, то происходит попытка входа, используя пароль (если попытка входа была и она вызвала ошибку SessionPasswordNeededError)

Возвращается True, если вход успешен, False, если требуется пароль, и строка, если произошла ошибка

Обрабатываемые ошибки:
SessionPasswordNeededError - стоит 2фа и требуется пароль
PhoneCodeInvalidError - неверный код
PasswordHashInvalidError - неверный пароль
'''
async def tg_sign_in(session, phone=None, code=None, phone_hash=None, password=None):
    client = TelegramClient(StringSession(session), app_id, app_hash)
    await client.connect()
    
    try:
        if password==None: #пароля нет - обычный вход
            await client.sign_in(phone=phone, code=code, phone_code_hash=phone_hash, password=password)
        else: #пароль есть - вход с паролем
            await client.sign_in(password=password)

        await client.disconnect()
        return True

    except SessionPasswordNeededError: #если требуется пароль
        await client.disconnect()
        return False

    except PhoneCodeInvalidError: #если код неверный
        await client.disconnect()
        return "Неверный код"

    except PasswordHashInvalidError: #если пароль неверный
        await client.disconnect()
        return "Неверный пароль"

    except Exception as e: #что-либо другое
        await client.disconnect()
        return str(e)