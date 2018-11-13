from django.urls import path, include 
from .views import *

urlpatterns = [
    path('', userHomePage, name='user_home'),
    path('delete_file/',deleteFile, name="delete_file"),
    path('upload/',fileUploadView,name='upload'),
    path('keywords/', keywordView, name='keyword'),
    path('display_summary/',displaySummaryView, name="display_summary_view"),
    path('grammar_check/',grammarCheckerView, name="grammar_checker_view"),
    path('download/',downloadView, name='download'),
    path('logout/',logout_page, name='logout'),
]
