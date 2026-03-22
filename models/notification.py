from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from users.person import Base


class Notification(Base):
    __tablename__ = 'notification'

    id = Column(Integer, primary_key=True)
    content = Column(String)
    status = Column(String, default="Unread")
    visit_id = Column(Integer, ForeignKey('visit.id'))

    visits = relationship("Visit", back_populates="notifications")
