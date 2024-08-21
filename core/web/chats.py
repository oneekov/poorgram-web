from django.http import HttpResponse
from django.shortcuts import render, redirect
from tg.account import getUsername

async def chats(request):
    #TODO: сделать тут чаты, вместо этой штуки для теста
    username = await getUsername(request.COOKIES["auth_key"])

    response = render(request, "chats.html", context={"username": username})
    return response