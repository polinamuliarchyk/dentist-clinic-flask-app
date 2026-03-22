from datetime import date
from typing import Optional

from sqlalchemy import Column, Integer, ForeignKey, String, Date
from sqlalchemy.orm import relationship

from users.person import Base


class WorkSchedule(Base):
    __tablename__ = 'work_schedule'

    id = Column(Integer, primary_key=True)
    date = Column(Date)
    time = Column(String)
    receptionist_id = Column(Integer, ForeignKey('receptionist.id'))

    receptionist = relationship("Receptionist", back_populates="workschedule")

    def edit_schedule(self, new_date: Optional[date] = None, new_time: Optional[str] = None, session=None) -> None:
        """
        Edits the work schedule – changes the date and/or time.

        Args:
            new_date (date, optional): The new work date.
            new_time (str, optional): The new time range (e.g. "08:00-16:00").
            session (Session, optional): An SQLAlchemy session object, required to save changes.
        """
        if not new_date and not new_time:
            raise ValueError("You must enter at least a new date or a new time.")

        if new_date:
            self.date = new_date
        if new_time:
            self.time = new_time

        if session:
            session.commit()