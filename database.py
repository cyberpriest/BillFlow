import os
from sqlalchemy.orm import sessionmaker 
from sqlalchemy import create_engine 
from sqlalchemy.ext.declarative import declarative_base 

DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///test.db')
connect_args = {'check_same_thread': False} if DATABASE_URL.startswith('sqlite') else {}
engine = create_engine(DATABASE_URL, echo=True, connect_args=connect_args)
SessonLocal =  sessionmaker(autoflush=False,autocommit=False ,bind=engine)

def get_db():
    db = SessonLocal()
    try:
        yield db 
    finally :
        db.close()


Base = declarative_base()