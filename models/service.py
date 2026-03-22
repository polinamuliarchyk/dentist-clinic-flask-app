from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship

from users.person import Base


class Service(Base):
    __tablename__ = 'service'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    price = Column(Float)
