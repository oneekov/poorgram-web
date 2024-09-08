from django.urls import path
from . import auth, chats, various

urlpatterns = [
    path('', auth.index),

    path('auth/code', auth.code),
    path('auth/2fa', auth.twofactor),
    path('auth/signin', auth.sign_in),
    path('auth/logout', auth.log_out),

    path('chats/', chats.chats),
    path('archive/', chats.archive),

    path('error/', various.error)
]