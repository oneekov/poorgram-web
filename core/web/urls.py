from django.urls import path
from . import auth, chats

urlpatterns = [
    path('', auth.index),
    path('auth/code', auth.code),
    path('auth/2fa', auth.twofactor),
    path('auth/signin', auth.sign_in),
    path('chats/', chats.chats)
]