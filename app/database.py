import psycopg2
import time

from .config import settings
from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# We are using SQLAlchemy to connect to our database
# But just for documentation purposes we just saved it for reference
# in case we ever want to run raw SQL directly using this Postgres library

# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='postgres', user='postgres', 
#             password='123', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection was successful")
#         break
#     except Exception as error:
#         print("Connecting to database failed")
#         print("Error: ", error)
#         # If I set up wrong password start uvicorn app.main:app --reload
#         # see this error, then change password to correct one I will still
#         # in the loop. Even Ctrl+C doesn't help. But in the video this code
#         # works fine: https://youtu.be/0sOvCWFmrtA?feature=shared&t=14803
#         time.sleep(2)
