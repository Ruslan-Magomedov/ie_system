from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base



DB_URL = "sqllite:///./finance.db"
engin = create_engine(DB_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engin, autoflush=False, expire_on_commit=False)

Base = declarative_base()