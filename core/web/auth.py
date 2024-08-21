#FIXME: Нужна куча проверок тут на валидность данных

from django.http import HttpResponse
from django.shortcuts import render, redirect
from tg.auth import send_code, tg_sign_in
# from core.settings import SECRET_KEY
import datetime

#TODO: Сделать проверки, чтобы челы не могли перескочить с главной на ввод пароля, например
#TODO: Сделать перенаправление на chats, если вход выполнен

async def index(request):
    return render(request, "index.html")

async def code(request):
    phone_hash, auth_key = await send_code(request.GET.get('number'))

    response = render(request, "code.html")
    response.set_cookie("phone_hash", phone_hash)
    response.set_cookie("number", request.GET.get('number'))
    response.set_cookie("auth_key", auth_key, max_age=9999999)
    return response

async def twofactor(request):
    result = await tg_sign_in(
        request.COOKIES['auth_key'],
        phone=request.COOKIES['number'],
        code=request.GET.get('code'),
        phone_hash=request.COOKIES['phone_hash']
    )

    if result: 
        response = redirect("chats/")
        response.delete_cookie("number")
        response.delete_cookie("phone_hash")
    else: 
        response = render(request, "2fa.html")
        response.set_cookie("code", request.GET.get('code'))
    
    return response

async def sign_in(request):
    await tg_sign_in(
        request.COOKIES['auth_key'],
        phone=request.COOKIES['number'],
        code=request.COOKIES['code'],
        phone_hash=request.COOKIES['phone_hash'],
        password=request.GET.get('password')
    )

    response = redirect("/chats/")
    response.delete_cookie("number")
    response.delete_cookie("phone_hash")
    response.delete_cookie("code")

    return response