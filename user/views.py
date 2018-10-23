from django.shortcuts import render

# Create your views here.

def userHomePage(request):
	return render(request,'user_home.html')

