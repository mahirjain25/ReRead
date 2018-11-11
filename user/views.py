from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.urls import reverse
from .forms import *
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect
from django.urls import reverse
from urllib.parse import urlencode
# from .views import *
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from gensim.summarization import keywords
from bs4 import BeautifulSoup
import requests
import time
from django.contrib.auth import logout


import os
import sys

from sys import argv
import nltk
#import language_check

# for querying arxiv
import urllib.request as request


# Create your views here.
@login_required(redirect_field_name='login')
def userHomePage(request):
	if request.method == "POST":
		file_name = request.POST.get('name', None)
		with open('user/files/' + request.user.username + '/' + file_name) as f:
			data = f.read()
		result = {
			'file_content' : data
		}
		return JsonResponse(result)

	if not(os.path.isdir('user/files/')):
		os.mkdir('user/files/')

	if not(os.path.isdir('user/files/'+request.user.username)):
		os.mkdir('user/files/'+request.user.username)
	
	file_list = os.listdir('user/files/'+request.user.username)
	return render(request,'user_home.html', {'files' : file_list,'username':request.user.username})
	
@login_required(redirect_field_name='login')
def logout_page(request):
	os.system("rm -rf "+os.getcwd()+"/user/files/"+request.user.username)
	logout(request)
	return HttpResponseRedirect('/')


@login_required(redirect_field_name='login')
def displayUploadedFile(request):
	if request.method == 'GET':
		file_name = request.GET.get('file_name')
		with open('user/files/' + request.user.username + '/' + file_name + '.txt') as f:
			data = f.read()
		return render(request, 'display_uploaded_file.html', {'content' : data})

@login_required(redirect_field_name='login')
def fileUploadView(request):
	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid():
			handle_uploaded_file(request.user.username,request.FILES['file'], form.cleaned_data['title'])
			return HttpResponseRedirect('/user')
	else:
		form = UploadFileForm()
	return render(request, 'upload.html', {
		'form': form
	})


def handle_uploaded_file(username, f, file_name):
	with open('user/files/'+username+'/'+ file_name + '.txt', 'wb+') as destination:
		for chunk in f.chunks():
			destination.write(chunk)  



def createSummaryFromFile(filepath,len_pct):
	inputFile, file_extension = filepath.split('.')
	print(inputFile)
	# if the input file is a pdf file
	if file_extension == "pdf":
		cmd = "pdftotext %s %s" % (inputFile + '.' + file_extension, inputFile + ".txt")
		os.system(cmd)
		inputFile = inputFile + ".txt"

	outputFile = inputFile + '_abtracted.txt'
	print(outputFile)
	bashCommand = "sumy lex-rank --length={}% --file={} >> {}".format(len_pct, inputFile+'.txt', outputFile)

	os.system(bashCommand)

def grammarChecker(filepath):
	inputFile, file_extension = filepath.split('.')
	out_file = inputFile + '_grammar_corrected.txt'

	if file_extension == "pdf":
		cmd = "pdftotext %s %s" % (inputFile + '.' + file_extension, inputFile + ".txt")
		os.system(cmd)

	f = open(inputFile + '.txt', 'r')

	s = f.read()
	tool = language_check.LanguageTool('en-US')
	matches = tool.check(s)
	language_check.correct(s, matches)
	f.close()

	new_f = open(out_file, 'w')
	new_f.write(s)
	new_f.close()


@login_required(redirect_field_name='login')
def displaySummaryView(request):
	if request.method == 'GET':
		pct = 30
		if request.GET.urlencode() == "":
			file_list = os.listdir('user/files/'+request.user.username)
			return render(request,'summary.html', {'files' : file_list,'username':request.user.username})
		else:
			filename = request.GET.get('filename','')
			print(filename)
			filepath = "/user/files/" + request.user.username + "/" + filename
			createSummaryFromFile(filepath,pct)
			return HttpResponseRedirect("/user")

@login_required(redirect_field_name='login')
def keywordView(request):
	file_name = request.GET.get('file_name')
	file_path = ('user/files/' + request.user.username + '/' + file_name + '.txt')
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




# parse input arguments
def get_relevant_papers(keyword_string):

	base_url = 'http://export.arxiv.org/api/query?' # base api query url
	print('Searching arXiv for %s' % (keyword_string, ))

	query = 'search_query=%s&sortBy=lastUpdatedDate' % (keyword_string)


	with request.urlopen(base_url+query) as answer:
		parse = feedparser.parse(answer)

	ans = {}
	
	for e in parse.entries:
		ans[e.title] = e.id


	if len(parse.entries) == 0:
		print('Received no results from arxiv. Rate limiting? Exiting. Restart later maybe.')
		# print(answer)
		

	return ans



