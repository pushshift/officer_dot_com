#!/usr/bin/env python3

import requests
from selectolax.parser import HTMLParser
import sys
import re
import time
import logging
import os.path
logging.basicConfig(level=logging.INFO)

BASE_URL = "https://forum.officer.com/"

def get_forum_html():
    '''Get the main page HTML and save to a file called html. If file already
    exists then do nothing'''
    if not os.path.isfile("html"):
        r = requests.get(BASE_URL)
        if r.ok:
            fh = open("html", "bw")
            fh.write(r.content)
        else:
            sys.exit()

def get_forum_data():
    '''Parse data for each forum present on main page'''
    html = open("html", "br").read()
    p = HTMLParser(html)
    forums = p.css("tr.forum-item")

    # Process each tr node with a class name of "forum-item"
    for forum in forums:
        forum_data = {}
        forum_data['topic_count'] = int(forum.css_first("td.topics-count").text().replace(',',''))
        forum_data['posts_count'] = int(forum.css_first("td.posts-count").text().replace(',',''))
        cell_forum = forum.css_first("td.cell-forum")
        forum_title_element = cell_forum.css_first("a.forum-title")
        forum_data['title'] = forum_title_element.text()
        forum_data['url'] = forum_title_element.attrs['href']
        logging.info(f"Forum data is: {forum_data}")


get_forum_html()
get_forum_data()

