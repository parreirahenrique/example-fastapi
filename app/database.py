from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()

# while True:
#     try:
#         # conn = psycopg2.connect(host = 'localhost', database = 'fastapi', user = input('Please, insert your user: '), password = input('Please, insert your password: '), cursor_factory=RealDictCursor)
#         conn = psycopg2.connect(host = 'localhost', database = 'fastapi', user = 'postgres', password = '181011977479He', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print('Database connection was succesfull!')
#         break
#     except Exception as error:
#         print('Connection with the database has failed.')
#         print('Error: ', error)
#         time.sleep(2)

# cursor.execute('''SELECT * FROM posts''')
# my_posts = cursor.fetchall()