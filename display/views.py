from django.shortcuts import render
from django.http import HttpResponse


def display(request):
    if request.method == 'GET':
    	file_name = request.GET.get('file_name')
    	with open('display/files/' + file_name + '.txt') as f:
    		data = f.read()
    	return render(request, 'content.html', {'content' : data})
