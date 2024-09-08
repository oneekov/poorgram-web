from django.http import HttpResponse
from django.shortcuts import render, redirect
from tg.chat import getChats
from .utils import errorRedirect

async def chats(request):
    chats = await getChats(request.COOKIES['auth_key'])

    if type(chats) == str:
        return await errorRedirect(chats)

    response = render(request, "chats.html", context={"dialogs": chats, "archive": False})
    return response

async def archive(request):
    chats = await getChats(request.COOKIES['auth_key'], folder=1)

    if type(chats) == str:
        return await errorRedirect(chats)

    response = render(request, "chats.html", context={"dialogs": chats, "archive": True})
    return response