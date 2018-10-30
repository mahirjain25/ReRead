from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse


def HomePageView(request):
	return render(request,'home.html')