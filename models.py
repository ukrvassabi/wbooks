import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Base = declarative_base()


class Book(Base):
    __tablename__ = "book"
    id = Column(Integer, primary_key=True)
    title = Column(String(250))
    link = Column(String(1000))
    created_on = Column(DateTime, default=datetime.datetime.utcnow)
    category_id = Column(Integer, ForeignKey("category.id"))
    category = relationship("Category", backref=backref("books", lazy="dynamic"))
    wbook = relationship("Wbook", uselist=False)

    def __repr__(self):
        return 'Book \t\t"%s"' % self.title


class Category(Base):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True)
    name = Column(String(250), unique=True)
    created_on = Column(DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return '=== Category \t"%s"' % self.name


class Wbook(Base):
    __tablename__ = "wbook"
    id = Column(Integer, primary_key=True)
    created_on = Column(DateTime, default=datetime.datetime.utcnow)
    wbook_id = Column(Integer, unique=True)
    book_id = Column(Integer, ForeignKey("book.id"))
    book = relationship("Book", backref=backref("wbooks", lazy="dynamic"))

    def __repr__(self):
        return 'Wbook \t\t"%s"' % self.wbook_id


if __name__ == "__main__":
    from sqlalchemy import create_engine
    from config import DATABASE_URI
    engine = create_engine(DATABASE_URI)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
