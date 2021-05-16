from datetime import date, timedelta

from sqlalchemy import desc, func, and_

from model.db_base import session
from model.record import Record

class DB_Controller:
    def __init__(self):
        pass

    def save_record(self, id, title, author, url, post_time):
        record = Record(id=id, title=title, author=author, url=url, post_time=post_time)

        session.add(record)  
        session.commit()

    def search_by_id(self, id):
        results = session.query(Record).filter_by(id=id)
        return results

    def search_by_keyword(self, keyword):
        days_ago = date.today() - timedelta(10)

        results = session.query(Record).filter(and_(func.lower(Record.title).contains(keyword.lower()), Record.post_time >= days_ago)).order_by(desc(Record.post_time)).limit(5).all()
        
        return_list = [(result.title, result.url) for result in results]
        
        return return_list
