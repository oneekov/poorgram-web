from django.http import HttpResponse
from django.shortcuts import render, redirect
from tg.auth import send_code, tg_sign_in, tg_log_out
from urllib.parse import urlencode
# from core.settings import SECRET_KEY
# import datetime

#TODO: Добавить возможность выйти из аккаунта

async def index(request):
    if 'auth_key' in request.COOKIES.keys(): #Если вход уже выполнен
        return redirect("/chats/")

    return render(request, "index.html")

async def code(request):
    phone_hash, auth_key = await send_code(request.GET.get('number', "+00000000007"))

    if phone_hash == 0: #если ошибка
        params = {'error': auth_key}

        return redirect("/error/?" + urlencode(params))

    response = render(request, "code.html")
    response.set_cookie("phone_hash", phone_hash)
    response.set_cookie("number", request.GET.get('number'))
    response.set_cookie("auth_key", auth_key, max_age=9999999)
    return response

async def twofactor(request):
    if any(cookie in request.COOKIES.keys() for cookie in ('auth_key', 'number', 'phone_hash')): #Если человек "перепрыгнул страницу" и один из куки отсутствует
        params = {'error': "Выйдите из сессии и попробуйте снова"}

        return redirect("/error/?" + urlencode(params))

    result = await tg_sign_in(
        request.COOKIES['auth_key'],
        phone=request.COOKIES['number'],
        code=request.GET.get('code', "00000"),
        phone_hash=request.COOKIES['phone_hash']
    )

    if type(result) == str:
        params = {'error': result}

        response = redirect("/error/?" + urlencode(params))

    elif result: 
        response = redirect("/chats/")
        response.delete_cookie("number")
        response.delete_cookie("phone_hash")
    
    else: 
        response = render(request, "2fa.html")
        response.set_cookie("code", request.GET.get('code'))
    
    return response

async def sign_in(request):
    if any(cookie in request.COOKIES for cookie in ('auth_key', 'number', 'phone_hash', 'code')): #Если человек "перепрыгнул страницу" и один из куки отсутствует
        params = {'error': "Выйдите из сессии и попробуйте снова"}

        return redirect("/error/?" + urlencode(params))
    
    result = await tg_sign_in(
        request.COOKIES['auth_key'],
        phone=request.COOKIES['number'],
        code=request.COOKIES['code'],
        phone_hash=request.COOKIES['phone_hash'],
        password=request.GET.get('password', "0")
    )

    if type(result) == str:
        params = {'error': result}

        response = redirect("/error/?" + urlencode(params))
    else:
        response = redirect("/chats/")
        response.delete_cookie("number")
        response.delete_cookie("phone_hash")
        response.delete_cookie("code")

    return response

async def log_out(request):
    response = redirect('/')

    if 'auth_key' in request.COOKIES.keys():
        await tg_log_out()
        response.delete_cookie('auth_key')

    return response