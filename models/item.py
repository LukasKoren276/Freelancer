from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from . import Base

from helpers.constants import Constants as Const


class Item(Base):
    __tablename__ = 'items'

    item_id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.project_id'), nullable=True)
    item_name = Column(String(255), nullable=False)
    item_note = Column(String(255), nullable=True)
    item_price_per_unit = Column(Integer, nullable=False)
    price_unit = Column(String(10), nullable=False)
    status = Column(String(10), default=Const.status_active, nullable=False)

    project = relationship('Project', back_populates='items')
    times = relationship('ItemTime', order_by='ItemTime.item_time_id', back_populates='item')
    invoices = relationship('Invoice', back_populates='item')

    def __repr__(self):
        return (f"<Item(id={self.item_id}, project_id={self.project_id}, item_name={self.item_name}'"
                f", item_price={self.item_price_per_unit}), item_price_unit={self.price_unit}>")

    __table_args__ = (
        UniqueConstraint('project_id', 'item_name', name='uix_project_item_name'),
    )
