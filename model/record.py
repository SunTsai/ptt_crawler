from sqlalchemy import Column, String, DateTime

from model.db_base import base

class Record(base):  
    __tablename__ = 'gamesale'

    id = Column(String, primary_key=True)
    title = Column(String)
    author = Column(String)
    url = Column(String)
    post_time = Column(DateTime(timezone=False))