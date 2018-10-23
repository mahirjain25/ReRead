from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse


# Create your views here.

def userHomePage(request):
	if request.user.is_authenticated:
		return render(request,'user_home.html')
	else:
		return HttpResponseRedirect(reverse('login'))

