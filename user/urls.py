from django.urls import path, include 
from .views import *

urlpatterns = [
    path('', userHomePage, name='user_home'),
    path('display_uploaded_file/',displayUploadedFile, name="display_uploaded_file"),
    path('upload/',fileUploadView,name='upload'),
]
