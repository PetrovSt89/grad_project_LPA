from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from src.config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME


engine = create_engine(f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

db_session = scoped_session(sessionmaker(bind=engine))
