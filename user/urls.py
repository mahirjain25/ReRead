from django.urls import path, include 
from .views import *

urlpatterns = [
    path('', userHomePage, name='user_home'),
    path('display_uploaded_file/',displayUploadedFile, name="display_uploaded_file"),
    path('upload/',fileUploadView,name='upload'),
    path('keywords/', keywordView, name='keyword'),
    path('display_summary/',displaySummaryView, name="display_summary_view"),
    path('logout/',logout_page, name='logout'),
]
