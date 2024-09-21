

from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from . import Base

class Price(Base):
    __tablename__ = 'prices'

    price_id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey('items.item_id'), nullable=False)
    price = Column(Integer, nullable=False)

    item = relationship('Item', back_populates='prices')

    def __repr__(self):
        return f"<Price(id={self.price_id}, item_id={self.item_id}, price={self.price})>"
