import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Находим путь к папке, в которой лежит этот файл (database.py)
basedir = os.path.abspath(os.path.dirname(__file__))

# Собираем правильный путь к базе данных
# Мы предполагаем, что папка 'instance' лежит в корне вашего проекта
db_path = os.path.join(basedir, "instance", "klinika.db")

# Используем f-строку для формирования пути
engine = create_engine(f"sqlite:///{db_path}", echo=True)

Base = declarative_base()
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)