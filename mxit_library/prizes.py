#!/usr/bin/python
from support_flask.models import Prize,CreateSession

def CheckPrizeExists(mxit_id):
	session_support = CreateSession()
	if session_support.query(Prize).filter_by(mxit_id=mxit_id,active=True,waiting_action=False).count() > 0:
		#Prize waiting
		return True
	else:
		return False