from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import time
from psycopg2.extras import RealDictCursor
import psycopg2
#from .config import settings

sqlalchemy_database_url= f"postgresql://postgres:8938@localhost:5432/FASTAPIdb"

#sqlalchemy_database_url= f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_username}"
engine = create_engine(sqlalchemy_database_url)

sessionlocal= sessionmaker(autocommit=False, autoflush=False, bind= engine)
Base=declarative_base()

#DEPENDENCY
def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()

# while True:
#     try :
#         conn=psycopg2.connect(host='localhost', database='FASTAPIdb' , user= 'postgres' , password= '8938', cursor_factory= RealDictCursor)
#         cursor=conn.cursor()
#         print('Connection to database succesfull')
#         break
#     except Exception as error:
#         print('Connection to database failed')
#         print('Error', error)
#         time.sleep(2)
