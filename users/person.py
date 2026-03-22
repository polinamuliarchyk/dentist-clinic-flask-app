from sqlalchemy import Column, Integer, String, Enum as SqlEnum, ForeignKey
from sqlalchemy.orm import relationship
from users.Enum import RoleEnum

from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Person(Base):
    __tablename__ = 'person'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    type = Column(String)

    roles = relationship("RoleEnumValue", back_populates="person", cascade="all, delete-orphan")

    __mapper_args__ = {
        "polymorphic_on": "type",
        "polymorphic_identity": "person"
    }


class RoleEnumValue(Base):
    __tablename__ = "role_enum_value"
    person_id = Column(Integer, ForeignKey("person.id"), primary_key=True)
    role = Column(SqlEnum(RoleEnum), primary_key=True)

    person = relationship("Person", back_populates="roles")
