from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine("sqlite:///instance/klinika.db", echo=True)

Base = declarative_base()

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)