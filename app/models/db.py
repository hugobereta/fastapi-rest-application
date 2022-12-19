from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Creates database in this same directory
SQL_ALCHEMY_DATABASE_URL = 'sqlite:///./data.db'

# This arg is only for SQLite
CONNECT_ARGS = {
    'check_same_thread': False,
}

engine = create_engine(
    SQL_ALCHEMY_DATABASE_URL,
    connect_args=CONNECT_ARGS,
    echo=True,
)

# sessionmaker is a factory
# SessionLocal is a class to represent database session when it is instantiated
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# The declarative_base return a class to create Base class.
# Later, we will inherit from this class to create each
# of the database models or classes(the ORM models).
Base = declarative_base()


# Creates an independent database session for each request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
