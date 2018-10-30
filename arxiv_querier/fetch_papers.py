"""
Queries arxiv API and downloads papers (the query is a parameter).
The script is intended to enrich an existing database pickle (by default db.p),
so this file will be loaded first, and then new results will be added to it.

Usage: get_relevant_papers(keywords separated by spaces)
"""

import os
import time
import pickle
import random
import argparse
import urllib.request as request
import feedparser
import http




# parse input arguments
def get_relevant_papers(keyword_string):
    parser = argparse.ArgumentParser()
    parser.add_argument('--search-query', type=str,
                        default='cat:cs.CV+OR+cat:cs.AI+OR+cat:cs.LG+OR+cat:cs.CL+OR+cat:cs.NE+OR+cat:stat.ML',
                        help='query used for arxiv API. See http://arxiv.org/help/api/user-manual#detailed_examples')
    parser.add_argument('--start-index', type=int, default=0, help='0 = most recent API result')
    parser.add_argument('--max-index', type=int, default=1, help='upper bound on paper index we will fetch')
    parser.add_argument('--results-per-iteration', type=int, default=1, help='passed to arxiv API')
    parser.add_argument('--wait-time', type=float, default=5.0, help='lets be gentle to arxiv API (in number of seconds)')
    parser.add_argument('--break-on-no-added', type=int, default=1, help='break out early if all returned query papers are already in db? 1=yes, 0=no')
    args = parser.parse_args()


    base_url = 'http://export.arxiv.org/api/query?' # base api query url
    print('Searching arXiv for %s' % (keyword_string, ))

    for i in range(args.start_index, args.max_index, args.results_per_iteration):
        print("Results %i - %i" % (i,i+args.results_per_iteration))

        query = 'search_query=%s&sortBy=lastUpdatedDate&start=%i&max_results=%i' % (keyword_string,
                                                                i, args.results_per_iteration)

        with request.urlopen(base_url+query) as answer:
            parse = feedparser.parse(answer)


        ans = {}

        for e in parse.entries:
            ans[e.title] = e.id

            # print('\Link to the research-paper: {}'.format(e.id))
            # print('\n\nAbstract of the research-paper: {}'.format(e.summary))
            # print(e)
            # print('\n{} \t {}'.format(e.title, e.id))
            # print('Authors of the research-paper: {}'.format(e.authors))



        if len(parse.entries) == 0:
            print('Received no results from arxiv. Rate limiting? Exiting. Restart later maybe.')
            print(answer)
            break

        return ans
