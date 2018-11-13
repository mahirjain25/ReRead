from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.urls import reverse
from .forms import *
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect, HttpResponse
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
import language_check
import feedparser
# for querying arxiv
import urllib.request as request


# Create your views here.
@login_required(redirect_field_name='login')
def userHomePage(request):
	if request.method == "POST":
		file_name = request.POST.get('name', None)
		with open('user/files/' + request.user.username + '/' + file_name) as f:
			data = f.read()
		data = "<br />".join(data.split("\n"))
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
def deleteFile(request):
	if request.method == 'GET':
		file_name = request.GET.get('filename')
		curr_dir = os.getcwd()
		os.chdir("user/files/"+request.user.username+"/")
		os.system("rm "+file_name)
		os.chdir(curr_dir)
		return HttpResponseRedirect("/user")

@login_required(redirect_field_name='login')
def downloadView(request):
	if request.method == 'GET':
		filename = request.GET.get('filename','')
		filepath = "user/files/"+request.user.username+"/"+filename
		print(filepath)
		if os.path.exists(filepath):
			with open(filepath, 'rb') as fh:
				response = HttpResponse(fh.read(), content_type="application/vnd.oasis.opendocument.text")
				response['Content-Disposition'] = 'inline; filename=' + os.path.basename(filepath)
				return response
		raise Http404

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
		'form': form,
		'username': request.user.username
	})


def handle_uploaded_file(username, f, file_name):
	with open('user/files/'+username+'/'+ file_name + '.txt', 'wb+') as destination:
		for chunk in f.chunks():
			destination.write(chunk)  

def grammarChecker(filepath,username):
	inputFile, file_extension = filepath.split('.')
	input_file_name = inputFile.split("/")[-1]
	out_file = input_file_name + '_grammar_corrected.txt'
	curr_dir = os.getcwd()
	os.chdir("user/files/"+username+"/")
	if file_extension == "pdf":
		cmd = "pdftotext %s %s" % (input_file_name + '.' + file_extension, input_file_name + ".txt")
		os.system(cmd)

	f = open(input_file_name + '.txt', 'r')

	s = f.read()
	tool = language_check.LanguageTool('en-US')
	matches = tool.check(s)
	s = language_check.correct(s, matches)
	f.close()

	new_f = open(out_file, 'w')
	new_f.write(s)
	new_f.close()
	os.chdir(curr_dir)


@login_required(redirect_field_name='login')
def grammarCheckerView(request):
	if request.method == 'GET':
		if request.GET.urlencode() == "":
			file_list = os.listdir('user/files/'+request.user.username)
			return render(request,'grammar.html', {'files' : file_list,'username':request.user.username})
		else:
			filename = request.GET.get('filename','')
			filepath = "/user/files/"+request.user.username+"/"+filename
			grammarChecker(filepath,request.user.username)
			return HttpResponseRedirect("/user")

# ==================== Summarisation ===========================

def createSummaryFromFile(filepath,len_pct,username):
	inputFile, file_extension = filepath.split('.')
	# if the input file is a pdf file
	if file_extension == "pdf":
		cmd = "pdftotext %s %s" % (inputFile + '.' + file_extension, inputFile + ".txt")
		os.system(cmd)
		inputFile = inputFile + ".txt"

	input_file_name = inputFile.split('/')[-1]
	outputFile = input_file_name + '_abtracted.txt'
	bashCommand = "sumy lex-rank --length={}% --file={} > {}".format(len_pct, input_file_name+'.txt', outputFile)
	curr_dir = os.getcwd()
	os.chdir("user/files/"+username+"/")
	os.system(bashCommand)
	print(bashCommand, os.getcwd())
	os.chdir(curr_dir)

@login_required(redirect_field_name='login')
def displaySummaryView(request):
	if request.method == 'GET':
		if request.GET.urlencode() == "":
			file_list = os.listdir('user/files/'+request.user.username)
			return render(request,'summary.html', {'files' : file_list,'username':request.user.username})
		else:
			filename = request.GET.get('filename','')
			pct = request.GET.get('pct','')
			pct = int(pct)
			print(filename, pct)
			filepath = "/user/files/" + request.user.username + "/" + filename
			createSummaryFromFile(filepath,pct,request.user.username)
			return HttpResponseRedirect("/user")

# ==============================================================


# ================ KeyWord Extraction Functions ================

@login_required(redirect_field_name='login')
def keywordView(request):
	if request.method == 'GET':
		file_list = os.listdir('user/files/'+request.user.username)
		if request.GET.urlencode() == "":
			return render(request,'keyword_extraction.html', {'files': file_list,'content':{}, 'username': request.user.username})
		else:
			file_name = request.GET.get('filename')
			file_path = ('user/files/' + request.user.username + '/' + file_name)
			info = get_keyword_info(file_path)
			papers = get_papers(file_path)
			print(info)
			return render(request, 'keyword_extraction.html', {'files':file_list, 'content' : info, 'papers' : papers, 'username':request.user.username})

def get_papers(file_path):
	word_list = get_keywords(file_path)
	keyword_string = " ".join(word_list)
	paper_dict = get_relevant_papers(keyword_string)
	# for i, j in paper_dict:
		# print('{} {}'.format(i, j))
	print(paper_dict)
	return paper_dict

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
	return link_list[0:3]

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



