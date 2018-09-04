from django.shortcuts import render,redirect
from django.http import *
from .forms import *
from django.conf import settings
from django.core.files.storage import FileSystemStorage
# Create your views here.

def HomePageView(request):
	return render(request,'home.html')

def fileUploadView(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = DocumentForm()
    return render(request, 'upload.html', {
        'form': form
    })

