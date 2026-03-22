from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from users.person import Base


class Recommendation(Base):
    __tablename__ = 'recommendation'

    id = Column(Integer, primary_key=True)
    text = Column(String)
    client_id = Column(Integer, ForeignKey('client.id'))
    labtest_id = Column(Integer, ForeignKey('labtest.id'))

    client = relationship("Client", back_populates="recommendations")
    labtest = relationship("Labtest", back_populates="recommendations")

    @classmethod
    def add_recommendation(cls, text: str, client_id: int, labtest_id: int, session) -> "Recommendation":
        """
        Adds a new recommendation to the database.

        Args:
            text (str): The text of the recommendation.
            client_id (int): The ID of the client to whom the recommendation belongs.
            labtest_id (int): The ID of the test to which the recommendation relates.
            session (Session): The SQLAlchemy session for performing the operation.

        Returns:
            Recommendation: The created recommendation object.
        """
        new_recommendation = cls(
            text=text,
            client_id=client_id,
            labtest_id=labtest_id
        )

        session.add(new_recommendation)
        session.commit()
        return new_recommendation
