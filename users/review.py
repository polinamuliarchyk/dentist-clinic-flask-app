from sqlalchemy import Column, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from users.person import Base


class Review(Base):
    __tablename__ = 'review'
    client_id = Column(Integer, ForeignKey('client.id'), primary_key=True)
    dentist_id = Column(Integer, ForeignKey('dentist.id'), primary_key=True)
    review = Column(Text)

    client = relationship("Client", back_populates="dentist_associations")
    dentist = relationship("Dentist", back_populates="client_associations")


    @classmethod
    def add_review(cls, session, client_id: int, dentist_id: int, text: str):
        """
        Adds or updates a client’s review of a dentist.

        Args:
            session (Session): SQLAlchemy session.
            client_id (int): ID of the client submitting the review.
            dentist_id (int): ID of the dentist the review concerns.
            text (str): The content of the review.

        Returns:
            Review: An updated or new review entry.
        """
        review = session.query(cls).filter_by(
            client_id=client_id,
            dentist_id=dentist_id
        ).first()

        if review:
            review.review = text
        else:
            review = cls(
                client_id=client_id,
                dentist_id=dentist_id,
                review=text
            )
            session.add(review)

        session.commit()
        return review