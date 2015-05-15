import os, sys, datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()
'''
class MACAddress(Base):
	__tablename__ = 'mac'
	# We need an id as address is not a good primary key, due to mutability.
	id = Column(Integer, primary_key=True)
	address = Column(String(17), nullable=False)

class SSID(Base):
	__tablename__ = 'ssid'
	id = Column(Integer, primary_key=True)
	# SSIDs have a 31 or 32 character limit in name length.
	name = Column(String(32), nullable=False)
'''
class Packet(Base):
	__tablename__ = 'packet'
	id = Column(Integer, primary_key=True)
	mac = Column(String(17), nullable=False)
	ssid = Column(String(32))
	time = Column(DateTime, default=datetime.datetime.now())
	signal = Column(Integer)

def createNewDatabase(filename):
	engine = create_engine('sqlite:///%s.db' % filename, convert_unicode=True)
	Base.metadata.create_all(engine)
