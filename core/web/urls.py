from django.urls import path
from . import auth

urlpatterns = [
    path('', auth.index)
]