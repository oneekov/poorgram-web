from telethon import TelegramClient
from telethon.types import User
from telethon.sessions import StringSession
from telethon.errors import *
from .config import app_hash, app_id

async def getChats(session, folder = 0):
    client = TelegramClient(StringSession(session), app_id, app_hash)
    await client.connect()

    try:
        response = []
        async for dialog in client.iter_dialogs(limit=50, folder=folder):
            #если аккаунт удалён
            if len(dialog.name) == 0: continue
            
            #если первого сообщения нет
            message = dialog.message.message if dialog.message.message != None else "Этот чат пуст. Напишите первое сообщение!"

            response += [[f"{str(dialog.unread_count) + ' непрочитанных | ' if dialog.unread_count != 0 else ''}{'закреплено | ' if dialog.pinned else ''}{dialog.date.strftime('%d.%m.%y %H:%M')}", #тут формируются кол-во непрочитанных (если есть), форматированное время и закреп, если есть
                        dialog.name,
                        message if len(message) < 150 else message[:150] + '...',
                        dialog.id]]

        await client.disconnect()
        return response

    except Exception as e:
        await client.disconnect()
        return f"Uncaught error: {e}"