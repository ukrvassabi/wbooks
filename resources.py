import requests
from flask_restful import Resource, reqparse, marshal_with, abort, fields, request
from sqlalchemy.exc import SQLAlchemyError

from config import CLIENT_ID, ACCESS_TOKEN, WUNDERLIST_API_ENDPOINT, WUNDERLIST_BOOKS_LIST
from db import session
from models import Category, Book, Wbook

parser = reqparse.RequestParser()
parser.add_argument("limit", type=int)

headers = {
    "X-Access-Token": ACCESS_TOKEN,
    "X-Client-ID": CLIENT_ID
}

category_fields = {
    "id": fields.Integer,
    "created_on": fields.DateTime,
    "name": fields.String
}

book_fields = {
    "id": fields.Integer,
    "created_on": fields.DateTime,
    "link": fields.String,
    "title": fields.String,
    "category": fields.Nested(category_fields)
}

wbook_fields = {
    "id": fields.Integer,
    "created_on": fields.DateTime,
    "book_id": fields.Integer,
    "wbook_id": fields.Integer
}


class BookListResource(Resource):
    @marshal_with(book_fields)
    def get(self):
        args = parser.parse_args()
        if args.limit:
            books = session.query(Book).order_by(Book.title).limit(args.limit).all()
        else:
            books = session.query(Book).order_by(Book.title).all()
        return books


class CategoriesListResource(Resource):
    @marshal_with(category_fields)
    def get(self):
        args = parser.parse_args()
        if args.limit:
            categories = session.query(Category).limit(args.limit).all()
        else:
            categories = session.query(Category).all()
        return categories


class WbookListResource(Resource):
    @marshal_with(wbook_fields)
    def get(self):
        args = parser.parse_args()
        if args.limit:
            wbooks = session.query(Wbook).limit(args.limit).all()
        else:
            wbooks = session.query(Wbook).all()
        return wbooks


class WbookResource(Resource):
    def get(self):
        args = parser.parse_args()
        r = requests.get(WUNDERLIST_API_ENDPOINT + "lists", headers=headers)
        if r.status_code != 200:
            abort(400, description="can't fetch lists from Wunderlist")
        lists = r.json()
        list_id = None
        for _list in lists:
            if _list.get("title") == WUNDERLIST_BOOKS_LIST:
                list_id = _list.get("id")
        if list_id:
            r = requests.get(("%s%s?list_id=%s" % (WUNDERLIST_API_ENDPOINT, "tasks", list_id)), headers=headers)
            if r.status_code != 200:
                abort(400, description="can't fetch tasks from Wunderlist")
            r = r.json()
            if args.limit:
                return r[:args.limit]
            else:
                return r
        return []

    def post(self):
        r = requests.get(WUNDERLIST_API_ENDPOINT + "lists", headers=headers)
        if r.status_code != 200:
            abort(400, description="can't fetch lists from Wunderlist")
        lists = r.json()
        list_id = None
        for _list in lists:
            if _list.get("title") == WUNDERLIST_BOOKS_LIST:
                list_id = _list.get("id")
        if list_id:
            task = {
                "list_id": list_id,
                "title": request.json.get("title")
            }
            r = requests.post(WUNDERLIST_API_ENDPOINT + "tasks", json=task, headers=headers)
            if r.status_code != 201:
                abort(400, description="can't add task to Wunderlist")
            task_id = r.json().get("id")
            if task_id:
                note = {
                    "task_id": task_id,
                    "content": "Link: %s\nCategory: %s" % (request.json.get("link"), request.json.get("category"))
                }
                r = requests.post(WUNDERLIST_API_ENDPOINT + "notes", json=note, headers=headers)
                if r.status_code != 201:
                    abort(400, description="can't add note to Wunderlist")
                wbook_id = r.json().get("id")
                db_wbook = session.query(Wbook).filter(Wbook.wbook_id == wbook_id).first()
                if not db_wbook:
                    try:
                        db_wbook = Wbook(wbook_id=wbook_id, book_id=request.json.get("id"))
                        session.add(db_wbook)
                        session.commit()
                    except SQLAlchemyError:
                        return abort(403, description="record was added previously")
                return r.json()
        return []


class WuserResource(Resource):
    def get(self):
        r = requests.get(WUNDERLIST_API_ENDPOINT + "user", headers=headers)
        if r.status_code != 200:
            abort(400, description="can't fetch user from Wunderlist")
        return r.json()
