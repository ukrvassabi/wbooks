import json

import markdown
import requests
from bs4 import BeautifulSoup

from config import FREE_PROGRAMMING_BOOK_URI


def get_category_block(_list):
    category_name = _list.previous_sibling.previous_sibling.text
    if category_name == "Index":
        return None
    books = []
    for item in _list.find_all('li'):
        link_el = item.find('a')
        if link_el is None:
            continue
        books.append({
            "title": link_el.text,
            "link": link_el['href']
        })
    return {
        category_name: books
    }


def fetch_data():
    f = requests.get(FREE_PROGRAMMING_BOOK_URI)
    html = markdown.markdown(f.text)
    bs_html = BeautifulSoup(html, "html.parser")
    book_lists = bs_html.find_all("ul", recursive=False)
    results = []
    for book_list in book_lists:
        category_block = get_category_block(book_list)
        if category_block:
            results.append(category_block)
    return json.dumps(results)
