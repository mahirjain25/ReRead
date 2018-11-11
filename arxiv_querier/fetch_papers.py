
import time
import pickle
import random
import argparse
import urllib.request as request
import feedparser
import http


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

ans = get_relevant_papers('quantum computer networks')
print(ans)
