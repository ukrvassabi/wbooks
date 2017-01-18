import json

from db import session
from fetch_books import fetch_data
from models import Category, Book


def populate_db():
    categories = json.loads(fetch_data())
    for category in categories:
        for key in category:
            db_category = session.query(Category).filter(Category.name == key).first()
            if not db_category:
                db_category = Category(name=key)
                session.add(db_category)
                session.commit()
            print(db_category)
            for book in category[key]:
                db_book = session.query(Book).filter(Book.title == book.get("title")).first()
                if not db_book:
                    db_book = Book(title=book.get("title"), link=book.get("link"),
                                   category_id=db_category.id)
                    session.add(db_book)
                    session.commit()
                print(db_book)


if __name__ == "__main__":
    populate_db()
