from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///books.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    series = Column('Series', String)
    title = Column('Title', String)
    author = Column('Author', String)
    published_year = Column('Published', Integer)
    date_last_read = Column('Last Read', Date)
    number_of_pages = Column('Pages', Integer)
    genre = Column('Genre', String)


    def __repr__(self):
        return f'Title: {self.title}, Author: {self.author}, Published: {self.published_year}'
    
    @property
    def series_title(self):
        return f"{self.series + ' Series ' if self.series else ''}{self.title}"


class LogEntry(Base):
    __tablename__ = 'log'

    id = Column(Integer, primary_key=True)
    book_id = Column(Integer)
    date = Column(Date)
    notes = Column(String)


    def __repr__(self):
        return f'Book ID: {self.book_id}, Date: {self.date}, Notes: {self.notes}'