from quart import request, render_template, Blueprint
from telethon import TelegramClient
from telethon.types import User
from telethon.sessions import StringSession
from telethon.errors import * #type: ignore
from modules.utils import error_redirect, represent_dialog_as_str
from config import *

chats = Blueprint('chats', __name__, url_prefix='/chats')

async def get_chats(session: str, folder: int = 0):
    client = TelegramClient(StringSession(session), API_ID, API_HASH)
    await client.connect()

    try:
        response = []
        async for dialog in client.iter_dialogs(limit=50, folder=folder):
            #если аккаунт удалён
            if len(dialog.name) == 0: continue 
            
            #если первого сообщения нет
            message = dialog.message.message if dialog.message.message != None else "Этот чат пуст. Напишите первое сообщение!"

            response += [[await represent_dialog_as_str(dialog),
                        dialog.name,
                        message if len(message) < 150 else message[:150] + '...',
                        dialog.id]]
        return response

    except Exception as e:
        return f"Uncaught error: {e}"
    finally:
        client.disconnect()

@chats.route('/')
async def default_chats():
    chats = await get_chats(request.cookies['auth_key'])

    if type(chats) == str:
        return await error_redirect(chats)

    response = await render_template("chats.html", dialogs=chats, archive=False)
    return response

@chats.route('/archive')
async def archive_chats():
    chats = await get_chats(request.cookies['auth_key'], folder = 1)

    if type(chats) == str:
        return await error_redirect(chats)

    response = await render_template("chats.html", dialogs=chats, archive=True)
    return response
