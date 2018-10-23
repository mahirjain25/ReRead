from django.urls import path, include 
from .views import *

urlpatterns = [
    path('', userHomePage, name='user_home'),
]
