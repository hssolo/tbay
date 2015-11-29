from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, DateTime, Float, Date, ForeignKey, create_engine
from datetime import datetime

engine = create_engine('postgresql://ubuntu:thinkful@localhost:5432/tbay')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()# explain this?


class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    start_time = Column(DateTime, default=datetime.utcnow)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)#Relationship with User (owner)
    bid_id = relationship("Bid", backref="item")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    items = relationship("Item", backref="owner")
    bids = relationship("Bid", backref="bidder") 

class Bid(Base):
    __tablename__ = "bids"
    id = Column(Integer, primary_key=True)
    price = Column(Float, nullable=False)
    bidder_id = Column(Integer, ForeignKey('users.id'), nullable=False)#Relationship with User (bidder)
    item_bid = Column(Integer, ForeignKey('items.id'), nullable=False)#Relationship with Item (item_bid)
    
Base.metadata.create_all(engine)     

hans = User(username="Hans Santos", password="hans")
bob = User(username="Bob Stevens", password="bob")
john = User(username="John Smith", password="john")

baseball = Item(name="Baseball", description="Official 2015 World Series Baseball")
baseball.owner = hans

bid1 = Bid(price=20, bidder_id=bob, item_bid=baseball)
# bid1.owner = bob
# baseball.bid = bid1
# baseball.bid_id.append(bid1)


bid2 = Bid(price=15, bidder_id=john, item_bid=baseball)
# bid2.bidder = john
# baseball.bid = bid2
# baseball.bid_id.append(bid2)



session.add_all([hans, bob, john]) ## what is this doing?
session.add(baseball)
session.add_all([bid1, bid2])
session.commit()

# print("\nITEM(BASEBALL)")
# print("\nbaseball.owner.items:")
# print(baseball.owner.items) #<type(obj)>
# for x in baseball.owner.items:
#      print(x.name)
     
# print("\nbaseball.owner.bids:")     
# print(baseball.bid_id) #<type(list)>

     
# print("\nbaseball.bid.price:")      

   
# item to user is one to many / each item can have one owner but each owner can have multiple items
# baseball.owner_id = hans.id
# baseball.owner = hans
# hans.items.append(baseball)


#------------------------------------------------------------------------------
#many to many

# pizza_topping_table = Table('pizza_topping_association', Base.metadata, 
#     Column('pizza_id', Integer, ForeignKey('pizza.id')), 
#     Column('topping_id', Integer, ForeignKey('topping.id'))
# )

# class Pizza(Base):
#     __tablename__ = 'pizza'
#     id = Column(Integer, primary_key=True)
#     name = Column(String, nullable=False)
#     toppings = relationship("Topping", secondary="pizza_topping_association", backref="pizzas")

# class Topping(Base):
#     __tablename__ = 'topping'
#     id = Column(Integer, primary_key=True)
#     name = Column(String, nullable=False)
    
# Base.metadata.create_all(engine)     

# peppers = Topping(name="Peppers")
# garlic = Topping(name="Garlic")
# chilli = Topping(name="Chilli")

# spicy_pepper = Pizza(name="Spicy Pepper")
# spicy_pepper.toppings = [peppers, chilli]

# vampire_weekend = Pizza(name="Vampire Weekend")
# vampire_weekend.toppings = [garlic, chilli]


# session.add_all([garlic, peppers, chilli, spicy_pepper, vampire_weekend])
# session.commit()

# for topping in vampire_weekend.toppings:
#     print(topping.name)

# for pizza in chilli.pizzas:
#     print(pizza.name)    
    
    
# ------------------------------------------------------------------------------    
#One To Many 

# class Manufacturer(Base):
#     __tablename__ = 'manufacturer'
#     id = Column(Integer, primary_key=True)
#     name = Column(String, nullable=False)
#     guitars = relationship("Guitar", backref="manufacturer")

# class Guitar(Base):
#     __tablename__ = 'guitar'
#     id = Column(Integer, primary_key=True)
#     name = Column(String, nullable=False)
#     manufacturer_id = Column(Integer, ForeignKey('manufacturer.id'),
#                              nullable=False)

# fender = Manufacturer(name="Fender")
# strat = Guitar(name="Stratocaster", manufacturer=fender)#how come manufacturer isnt capitalized?
# tele = Guitar(name="Telecaster", manufacturer=fender) #or #fender.guitars.append(tele)
 
 
# session.add_all([fender, strat, tele])
# session.commit()
# print(fender.guitars)
# for guitar in fender.guitars:
#     print(guitar.name)
# print(tele.manufacturer.name)
# print(strat.manufacturer.id)
 

# ------------------------------------------------------------------------------

#Questions:

#  >>> user = session.query(User.id, User.username).all()
# >>> print(user)
# [(2, 'hsantos'), (3, 'asantos')]
# >>> user = session.query(User.username).filter(User.username == 'asantos').all()
# >>> print(user)
# [('asantos',)]
# >>> user.username = "anasantos"
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
# AttributeError: 'list' object has no attribute 'username'

# >>> user = session.query(User).filter(User.username == 'asantos').all()
# >>> print(user)
# [<tbay.User object at 0x7f3f3a6524e0>]
# >>> user.username = "anasantos"
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
# AttributeError: 'list' object has no attribute 'username'

# >>> user = session.query(User).get(3)
# >>> print(user)
# <tbay.User object at 0x7f3f3a6524e0>
# >>> user.username = "anasantos"
# >>> print(user.username)
# anasantos

#Answer:
#The usrname variable(or attribute) belongs to the class not the instance of the class.
