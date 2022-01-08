from enum import unique

from database import Base
from sqlalchemy import String,Boolean,Integer,Column,Text

class Item(Base):  #serilizer
    __tablename__ ='items'
    id = Column(Integer, primary_key=True)
    name=Column(String(255),nullable=False,unique=True)
    description=Column(Text)
    price=Column(Integer,nullable=False)
    on_offer=Column(Boolean,default=False)
#from models import Item
#new_item = Item(name="milk", description="nice milk", price = 200, on_offer = False)

def __repr__(self):
    return f"<Item name={self.name} price={self.price}>"