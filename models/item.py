from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from . import Base


class Item(Base):
    __tablename__ = 'items'

    item_id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.project_id'), nullable=True)
    item_name = Column(String(255), nullable=False)
    item_note = Column(String(255), nullable=True)

    project = relationship('Project', back_populates='items')
    times = relationship('ItemTime', order_by='ItemTime.item_time_id', back_populates='item')
    prices = relationship('Price', back_populates='item')

    def __repr__(self):
        return f"<Item(id={self.item_id}, project_id={self.project_id}, item_name={self.item_name})>"

    __table_args__ = (
        UniqueConstraint('project_id', 'item_name', name='uix_project_item_name'),
    )
