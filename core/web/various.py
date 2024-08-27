from django.http import HttpResponse
from django.shortcuts import render, redirect

async def about(request):
    pass #TODO: Сделать "о проекте"

async def privacy(request):
    pass #TODO: Сделать политику конфидициальности

#TODO: сделать проверку от гениев, которые решат перейти по ссылке без параметров
async def error(request):
    data = {'error': request.GET.get('error')}

    return render(request, 'error.html', context=data)