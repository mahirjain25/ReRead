from django.urls import path, include 
from .views import *

urlpatterns = [
    path('', userHomePage, name='user_home'),
    path('display_uploaded_file/',displayUploadedFile, name="display_uploaded_file"),
    path('upload/',fileUploadView,name='upload'),
<<<<<<< HEAD
    path('keywords/', keywordView, name='keyword')
=======
    path('display_summary/',displaySummaryView, name="display_summary_view"),
>>>>>>> 3daee52b8c08713b3eb864b7744dcc17bab9b02d
]
