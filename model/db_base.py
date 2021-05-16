from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base  

db_string = 'postgresql://suntsai@localhost:5432/ptt'

db = create_engine(db_string)  
base = declarative_base()

Session = sessionmaker(db)  

session = Session()

base.metadata.create_all(db)