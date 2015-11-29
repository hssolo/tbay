#One to One
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, DateTime, Float, Date, ForeignKey, create_engine
from datetime import datetime

engine = create_engine('postgresql://ubuntu:thinkful@localhost:5432/tbay')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()# explain this
class Person(Base):
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    passport = relationship("Passport", uselist=False, backref="owner")# uselist == single obj. rather than list of obj. 
    
class Passport(Base):
    __tablename__ = 'passport'
    id = Column(Integer, primary_key=True)
    issue_date = Column(Date, nullable=False, default=datetime.utcnow)
    owner_id = Column(Integer, ForeignKey('person.id'), nullable=False)
    #The foreign key constraint specifies that a matching value must exist in a specified column of a different table. In this case the owner ID must be a value which exists in 'person.id'; the id column of the person table.

Base.metadata.create_all(engine) 

beyonce = Person(name="Beyonce Knowles")
passport = Passport()
beyonce.passport = passport
session.add(beyonce)
session.commit()

print(beyonce.passport.issue_date)
print(passport.owner.name)    
              
     