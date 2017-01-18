import os
basedir = os.path.abspath(os.path.dirname(__file__))

DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'books.db')
FREE_PROGRAMMING_BOOK_URI = \
    "https://raw.githubusercontent.com/vhf/free-programming-books/master/free-programming-books.md"

CLIENT_ID = os.getenv("WUNDERLIST_CLIENT_ID", "add you Wunderlist client id here or set as env variable")
CLIENT_SECRET = os.getenv("WUNDERLIST_CLIENT_SECRET", "add you Wunderlist client secret here or set as env variable")
ACCESS_TOKEN = os.getenv("WUNDERLIST_ACCESS_TOKEN", "add you Wunderlist access token here or set as env variable")
WUNDERLIST_API_ENDPOINT = "https://a.wunderlist.com/api/v1/"
WUNDERLIST_BOOKS_LIST = "Books"
