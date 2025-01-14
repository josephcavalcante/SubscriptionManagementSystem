import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlmodel import SQLModel, create_engine
from models.model import Subscription, Payments

sqlite_file_name = 'database.db'
sqlite_url = f'sqlite:///{sqlite_file_name}'

engine = create_engine(sqlite_url, echo=False)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

if __name__ == '__main__':
    create_db_and_tables()