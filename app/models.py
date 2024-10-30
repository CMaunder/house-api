from sqlalchemy import Table, Boolean, Column, Integer, String, Float, DateTime

from .core.database import Base

class Dht11Record(Base):
    __tablename__ = "dht11_data"
    id = Column(Integer, primary_key= True, index=True)
    temp = Column(Float)
    humidity = Column(Float)
    room = Column(String)
    recorded_at = Column(DateTime)
    inserted_at = Column(DateTime)
