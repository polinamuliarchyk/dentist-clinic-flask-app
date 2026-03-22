from sqlalchemy import Column, Integer, ForeignKey, String, CheckConstraint
from sqlalchemy.orm import relationship

from users.person import Base


class Labtest(Base):
    __tablename__ = 'labtest'

    id = Column(Integer, primary_key=True)
    description = Column(String)

    dentist_id = Column(Integer, ForeignKey('dentist.id'), nullable=True)
    assistant_id = Column(Integer, ForeignKey('assistant.id'), nullable=True)

    dentist = relationship('Dentist', back_populates='labtests')
    assistant = relationship('Assistant', back_populates='labtests')
    recommendations = relationship("Recommendation", back_populates="labtest", cascade="all, delete-orphan")

    __table_args__ = (
        CheckConstraint(
            "(dentist_id IS NULL AND assistant_id IS NOT NULL) OR "
            "(dentist_id IS NOT NULL AND assistant_id IS NULL)",
            name="check_xor_dentist_assistant"
        ),
    )

    @classmethod
    def add_labtest(cls, description: str, dentist_id: int = None, assistant_id: int = None, session=None):
        """
        Creates and saves a new labtest to the database.

        Args:
            description (str): Description of the labtest.
            dentist_id (int, optional): ID of the assigned dentist.
            assistant_id (int, optional): The ID of the assigned assistant.
            session (Session): An SQLAlchemy Session object (required).

        Returns:
            Labtest: The created labtest object.
        """
        if session is None:
            raise ValueError("The session must be specified.")

        new_labtest = cls(
            description=description,
            dentist_id=dentist_id,
            assistant_id=assistant_id
        )

        session.add(new_labtest)
        session.commit()

        return new_labtest
