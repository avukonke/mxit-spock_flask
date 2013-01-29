#!/usr/bin/python

from boto.rds import RDSConnection,DBSecurityGroup
from auth import AWS_ACCESS_KEY,AWS_SECRET_ACCESS_KEY
from getmyip import GetMyIP
#Opens access for an IP address to the server.
class RDS():
	def __init__(self,ip=None):
		self.connection = RDSConnection(AWS_ACCESS_KEY,AWS_SECRET_ACCESS_KEY,validate_certs=False)
		self.ip = ip
		self.db_security_group = DBSecurityGroup(self.connection,name="default")
	def authorize_ip(self):
		if self.ip == None:
			g = GetMyIP()
			self.ip = g.get_my_ip()
		self.db_security_group.authorize("%s/32" % self.ip)

	def deauthorize_ip(self):
		if self.ip != None:
			self.db_security_group.revoke("%s/32" % self.ip)
		else:
			raise Exception

if __name__ == "__main__":
	#RDS 
	rds = RDS()
	print "Authorising IP."
	rds.authorize_ip()
	print "IP Authorised. Press Control-C to deauthorize the IP."
	while 1:
		try:
			from time import sleep
			sleep(60)
		except KeyboardInterrupt:
			print "Deauthorising IP."
			rds.deauthorize_ip()
			print "IP Deauthorised."
			break