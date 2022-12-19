from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQL_ALCHEMY_DATABASE_URL = 'sqlite:///./data.db'

CONNECT_ARGS = {
    'check_same_thread': False,
}

engine = create_engine(
    SQL_ALCHEMY_DATABASE_URL,
    connect_args=CONNECT_ARGS,
    echo=True,
)

session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

base = declarative_base()


def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()
