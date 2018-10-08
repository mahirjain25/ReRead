from django.shortcuts import render,redirect
from django.http import *
from .forms import *
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect
from django.urls import reverse
from urllib.parse import urlencode
from display import views as display_views


# Create your views here.

def HomePageView(request):
	return render(request,'home.html')

def fileUploadView(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'], form.cleaned_data['title'])
            base_url = reverse(display_views.display)
            query_string = urlencode({'file_name' : form.cleaned_data['title']})
            url = '{}?{}'.format(base_url, query_string)
            return HttpResponseRedirect(url)
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {
        'form': form
    })

def handle_uploaded_file(f, file_name):
    with open('display/files/' + file_name + '.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)