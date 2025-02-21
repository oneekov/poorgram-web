from quart import Blueprint, request, render_template, make_response
from telethon.sessions import StringSession
from telethon import TelegramClient
from telethon.errors import * #type: ignore
from modules.utils import *
from config import *

auth = Blueprint('auth', __name__, url_prefix='/auth')

async def send_code(phone):
    session = StringSession()
    client = TelegramClient(session, API_ID, API_HASH)
    await client.connect()

    try:
        login_token = await client.send_code_request(phone)
        return login_token.phone_code_hash, session.save()
    except PhoneNumberInvalidError: #Если номер неверный
        return 0, "Неверный номер"
    except FloodWaitError as e: #если Flood Wait
        return 0, f"Попробуйте через {e.seconds} секунд"
    except Exception as e: #Если что-то другое
        return 0, f"Uncaught error: {e}"
    finally:
        client.disconnect()

async def sign_in_telegram(session, phone: str = '', code: str = '', phone_hash: str = '', password: str = ''):
    client = TelegramClient(StringSession(session), API_ID, API_HASH)
    await client.connect()
    
    try:
        if password == '': #пароля нет - обычный вход
            await client.sign_in(phone = phone, code = code, phone_code_hash = phone_hash, password = password)
        else: #пароль есть - вход с паролем
            await client.sign_in(password = password)

        return True
    except SessionPasswordNeededError: #если требуется пароль
        return False
    except PhoneCodeInvalidError: #если код неверный
        return "Неверный код"
    except PasswordHashInvalidError: #если пароль неверный
        return "Неверный пароль"
    except Exception as e: #что-либо другое
        return str(e)
    finally:
        client.disconnect()

async def log_out_telegram(session):
    client = TelegramClient(StringSession(session), API_ID, API_HASH)
    await client.connect()
    await client.log_out()
    client.disconnect()

@auth.route('/code')
async def code():
    if not 'number' in request.args:
        return redirect('/')

    phone_hash, auth_key = await send_code(request.args.get('number'))
    
    if phone_hash == 0: # Переиспользование переменных :troll:
        return await error_redirect(auth_key)
    
    response = await make_response(await render_template('code.html'))
    response.set_cookie("phone_hash", phone_hash)
    response.set_cookie("number", request.args.get('number', '+00000000007'))
    response.set_cookie("auth_key", auth_key, max_age=1200000000)
    return response

@auth.route('/2fa')
async def twofactor():
    if not any(cookie in request.cookies.keys() for cookie in ('auth_key', 'number', 'phone_hash')):
        return await error_redirect("Выйдите из сессии и попробуйте снова")

    result = await sign_in_telegram(
        request.cookies['auth_key'],
        phone=request.cookies['number'],
        code=request.args.get('code', "00000"),
        phone_hash=request.cookies['phone_hash']
    )

    if type(result) == str:
        return await error_redirect(result)
    elif result: 
        response = redirect("/chats/")
        response.delete_cookie("number")
        response.delete_cookie("phone_hash")
    else:
        response = await make_response(await render_template("2fa.html"))
        response.set_cookie("code", request.args.get('code', '00000'))
    
    return response

@auth.route('/signin')
async def sign_in():
    if not any(cookie in request.cookies for cookie in ('auth_key', 'number', 'phone_hash', 'code')):
        return await error_redirect("Выйдите из сессии и попробуйте снова")
    
    result = await sign_in_telegram(
        request.cookies['auth_key'],
        phone=request.cookies['number'],
        code=request.cookies['code'],
        phone_hash=request.cookies['phone_hash'],
        password=request.args.get('password', '0')
    )

    if type(result) == str:
        return await error_redirect(result)
    else:
        response = redirect("/chats/")
        response.delete_cookie("number")
        response.delete_cookie("phone_hash")
        response.delete_cookie("code")

    return response

@auth.route('/logout')
async def log_out():
    response = redirect('/')

    if 'auth_key' in request.cookies.keys():
        await log_out_telegram(request.cookies['auth_key'])
        response.delete_cookie('auth_key')

    return response
