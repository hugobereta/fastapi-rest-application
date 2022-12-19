from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from app.models.db import Base


# Item model
class Item(Base):
    # Database table mapped
    __tablename__ = 'ITEMS'

    # Items columns
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(80), nullable=False, unique=True, index=True)
    price = Column(Float(precision=2), nullable=False)
    description = Column(String(200))
    store_id = Column(Integer, ForeignKey('STORES.id'), nullable=False)

    def __repr__(self):
        return f'ItemModel(name={self.name}, ' \
               f'price={self.price}, ' \
               f'store_id={self.store_id})'


# Store model
class Store(Base):
    # Table mapped
    __tablename__ = 'STORES'

    # Store columns
    # items is a foreign key in Items table
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(80), nullable=False, unique=True)
    items = relationship(
        'Item',
        primaryjoin='Store.id == Item.store_id',
        cascade='all, delete-orphan',
    )

    def __repr__(self):
        return f'Store(name={self.name}'
