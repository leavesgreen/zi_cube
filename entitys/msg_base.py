#coding=utf8

__author__ = 'alex'


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base




Base = declarative_base()

engine = create_engine("sqlite:///./temp.db",echo=True) #每月换一个?

Session = sessionmaker(bind=engine)

#Base.metadata.create_all(engine)



def get_session():
    return Session()

def createdb():
    Base.metadata.create_all(engine)
