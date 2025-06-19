from sqlalchemy import Column, Integer, String, Enum
from .database import Base
import enum

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False)  # 'admin' or 'viewer'

class StatusEnum(enum.Enum):
    in_stock = 'in stock'
    low_stock = 'low stock'
    ordered = 'ordered'
    discontinued = 'discontinued'

class InventoryItem(Base):
    __tablename__ = 'inventory_items'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    category = Column(String, nullable=False)
    status = Column(Enum(StatusEnum), nullable=False) 