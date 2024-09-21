from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from . import Base


class ItemTime(Base):
    __tablename__ = 'item_times'

    item_time_id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey('items.item_id'), nullable=False)
    time_from = Column(DateTime, nullable=False)
    time_to = Column(DateTime, nullable=False)
    duration_seconds = Column(Integer, nullable=False)
    item_time_note = Column(String(255))

    item = relationship('Item', back_populates='times')

    @property
    def duration(self) -> int:
        return int(round((self.time_to - self.time_from).total_seconds()))

    def __repr__(self) -> str:
        return (f"<ItemTime(id={self.item_time_id}, item_id={self.item_id}, "
                f"time_from={self.time_from}, time_to={self.time_to}, duration={self.duration})>")
