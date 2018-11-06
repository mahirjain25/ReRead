from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import *
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect
from django.urls import reverse
from urllib.parse import urlencode
from .views import *
from django.contrib.auth.decorators import login_required
from gensim.summarization import keywords
from bs4 import BeautifulSoup
import requests
import time


import os
import sys


# Create your views here.
@login_required(redirect_field_name='login')
def userHomePage(request):
	if not(os.path.isdir('user/files/'+request.user.username)):
		os.mkdir('user/files/'+request.user.username)
	return render(request,'user_home.html')
	

@login_required(redirect_field_name='login')
def displayUploadedFile(request):
	if request.method == 'GET':
		file_name = request.GET.get('file_name')
		with open('user/files/' + file_name + '.txt') as f:
			data = f.read()
		return render(request, 'display_uploaded_file.html', {'content' : data})

@login_required(redirect_field_name='login')
def fileUploadView(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'], form.cleaned_data['title'])
            base_url = '/user/keywords/'
            query_string = urlencode({'file_name' : form.cleaned_data['title']})
            url = '{}?{}'.format(base_url, query_string)
            return HttpResponseRedirect(url)
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {
        'form': form
    })


def handle_uploaded_file(f, file_name):
    with open('user/files/' + file_name + '.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

@login_required(redirect_field_name='login')
def keywordView(request):
    file_name = request.GET.get('file_name')
    file_path = ('user/files/' + file_name + '.txt')
    info = get_keyword_info(file_path)
    print(info)
    return render(request, 'keyword_extraction.html', {'content' : info})

# ================ KeyWord Extraction Functions ================

def get_keywords(file_path):
    fp = open(file_path, 'r+')
    content = fp.read()
    return keywords(content).split()

def get_google_links(string):
    link_list = []
    string = string.replace(' ', '+')
    URL = 'https://www.google.com/search?q=' + string
    page  = requests.get(URL)
    page_data = page.text
    page_soup = BeautifulSoup(page_data, 'lxml')
    links = page_soup.findAll('h3', {'class' : 'r'})
    for link in links:
        if link.find('a') is not None:
            link_list.append(link.find('a')['href'][7:])
    return link_list

def get_keyword_info(FILE_PATH):
    word_list = get_keywords(FILE_PATH)
    word_link_dict = {}
    for word in word_list:
        word_links = get_google_links(word)
        word_link_dict[word] = word_links
        time.sleep(0.5)                             # To prevent IP ban 
    return word_link_dict

# ==============================================================


