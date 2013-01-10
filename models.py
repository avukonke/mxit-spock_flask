#!/usr/bin/python
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String,ForeignKey,PickleType, Boolean
from sqlalchemy.orm import relationship, backref

Base = declarative_base()

from sqlalchemy import create_engine
from config import MYSQL_DB

db_engine = create_engine(MYSQL_DB,pool_recycle=60)

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=db_engine)
session = Session()

class MxitUser(Base):
	"""	A MxitUser class that authenticates every user,
		and if does not exist is created.
	"""
	__tablename__ = "mxituser"

	id = Column(Integer,primary_key=True)
	mxit_id = Column(String(255))
	mxit_nick = Column(String(255))
	points = Column(Integer)
	games_played = Column(Integer)

	def __init__(self, mxit_id,mxit_nick):
		self.mxit_id = mxit_id
		self.mxit_nick = mxit_nick
		self.points = 0
		self.games_played = 0

	def __repr__(self):
		return "<User('%s','%s')>" % (self.mxit_id,self.mxit_nick)


if __name__ == "__main__":
	"""Create the Database.
	"""
	import sys
	if "create" in sys.argv:
		print "Creating Database."
		Base.metadata.create_all(db_engine)
		print "Database Created."
	if "recreate" in sys.argv:
		print "Recreating Database."
		Base.metadata.drop_all(db_engine)
		Base.metadata.create_all(db_engine)
		print "Database Recreated."

		print "usage models.py\ncreate Creates a new Database \nrecreate Recreates a Database"