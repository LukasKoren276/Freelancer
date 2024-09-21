from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from . import Base


class Project(Base):
    __tablename__ = 'projects'

    project_id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'), nullable=False)
    project_name = Column(String(255), nullable=False)

    customer = relationship('Customer', back_populates='projects')
    items = relationship('Item', order_by='Item.item_id', back_populates='project')
    invoices = relationship('Invoice', back_populates='project', uselist=False)

    def __repr__(self):
        return f"<Project(id={self.project_id}, project name={self.project_name} customer_id={self.customer_id})>"

    __table_args__ = (
        UniqueConstraint('customer_id', 'project_name', name='uix_project_customer_name'),
    )