import urllib.request

url = 'http://export.arxiv.org/api/query?search_query=all:electron&start=0&max_results=1'



with urllib.request.urlopen(url) as query:
    s = query.read()
#I'm guessing this would output the html source code?
print(s)