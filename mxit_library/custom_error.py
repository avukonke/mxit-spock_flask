#!/usr/bin/python

from logging.handlers import SMTPHandler
from boto.ses.connection import SESConnection
from auth import AWS_ACCESS_KEY,AWS_SECRET_ACCESS_KEY

def SendEmail(to,subject,message,from_addr="server-action@rationalproducts.co.za",format="html"):
	conn = SESConnection(AWS_ACCESS_KEY,AWS_SECRET_ACCESS_KEY)
	conn.send_email(from_addr,subject,message,to,format=format)

class SESHandler(SMTPHandler):
	""" Send's an email using BOTO SES.
	"""
	def emit(self,record):
		conn = SESConnection(AWS_ACCESS_KEY,AWS_SECRET_ACCESS_KEY)
		conn.send_email(self.fromaddr,self.subject,self.format(record),self.toaddrs)

if __name__ == "__main__":
	#Test
	import logging
	logger = logging.getLogger()
	mail_handler = SESHandler(mailhost="",fromaddr='server-error@rationalproducts.co.za',toaddrs="rodneyhawkins@gmail.com", subject='Blackjack_Flask - Error')
	mail_handler.setLevel(logging.ERROR)
	logger.addHandler(mail_handler)
	try:
		1/0
	except:
		logger.exception("FFFFFFFFFFFFFFFFFFFFFFFUUUUUUUUUUUUUUUUUUUUUU")