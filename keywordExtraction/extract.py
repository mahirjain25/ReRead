from gensim.summarization import keywords
from bs4 import BeautifulSoup
import requests
import time

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
    place_soup = BeautifulSoup(page_data, 'lxml')
    place_soup
    links = place_soup.findAll('h3', {'class' : 'r'})
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
        time.sleep(0.5)
    return word_link_dict

if __name__ == "__main__":
    # Change this to path of desired text document
    FILE_PATH = 'file.txt'
    links = get_keyword_info('file.txt')
    print(links)
