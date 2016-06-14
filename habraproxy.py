# coding: utf-8

import re
import requests
import webbrowser

from bs4 import BeautifulSoup
from bs4.element import NavigableString

from flask import Flask


app = Flask(__name__)

BASE_REMOTE_DOMAIN = 'habrahabr.ru'
BASE_LOCAL_DOMAIN = '127.0.0.1:5000'


def process_string(s):
    w_list = set(re.findall(r'\b[\w]{6}\b', s, re.UNICODE))
    
    for word in w_list:
        s = s.replace(word, word+u"\u2122")
    return s

def replace_words(data):
    bs = BeautifulSoup(data, 'html.parser')
    for t in bs.find_all():
        if t.name == 'a' and t.get('href', 0):
            t['href'] = t['href'].replace(BASE_REMOTE_DOMAIN, BASE_LOCAL_DOMAIN)
        if t.name not in ('style', 'script'):
            for s in t.contents:
                if isinstance(s, NavigableString):
                    s.string.replace_with(process_string(s.string))
    return str(bs)

@app.route('/')
def index():
    return """
        It's alive!

        <a href="http://%s/company/yandex/blog/258673/">Test link</a>


    """ % BASE_LOCAL_DOMAIN

@app.route('/<path:path>', methods=['GET'])
def site(path):
    full_path = "http://habrahabr.ru/{0}".format(path)
    page_content = requests.get(full_path).content
    return replace_words(page_content)


if __name__ == "__main__":
    webbrowser.open('http://'+BASE_LOCAL_DOMAIN)
    app.run(debug=True)
