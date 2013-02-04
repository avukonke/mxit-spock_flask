#!/usr/bin/python
import requests

class Shink(object):
	def __init__(self, auid, request_headers, remote_addr):
		self.gender = False
		self.age = False
		self.device = False
		self.country = False
		self.headers = {}
		if 'X-Forwarded-For' in request_headers:
			self.headers['X-Forwarded-For'] = request_headers['X-Forwarded-For']
		self.headers["REMOTE_ADDR"] = remote_addr
		if "X-Mxit-Profile" in request_headers:
			profile_from = request_headers["X-Mxit-Profile"]
			self.gender = profile_from.split(",")[3]
			from datetime import datetime
			self.age = int(int((datetime.today() - datetime.strptime(profile_from.split(",")[2], "%Y-%m-%d")).days) / 365.25)
			self.device = request_headers["X-Device-User-Agent"]
			self.country = profile_from.split(",")[1]
		else:
			if 'User-Agent' in request_headers:
				self.device = request_headers["User-Agent"]
			self.country = "ZA"
			#http://ox-d.shinka.sh/ma/1.0/arj?auid=318867&c.age=35&c.gender=male&c.device=android&c.country=za

		qs = ""
		if self.age:
			qs += "c.age=%s&" % self.age
		if self.gender:
			qs += "c.gender=%s&" % self.gender
		if self.device:
			qs += "c.device=%s&" % self.device
		if self.country:
			qs += "c.country=%s&" % self.country

		#print 'http://ox-d.shinka.sh/ma/1.0/arj?auid=%s&%s' % (auid,qs)
		if self.device != False:
			self.headers['User-Agent'] = "Mozilla Compatible/%s" % self.device
		else:
			self.device = "Mozilla Compatible"
		ad = requests.get('http://ox-d.shinka.sh/ma/1.0/arj?auid=%s&%s' % (auid, qs), headers=self.headers)	 # To serve diverse ads
		#print ad.json()
		try:
			impression = requests.get(ad.json()['ads']['ad'][0]['creative'][0]['tracking']['impression'], headers=self.headers)
			print "Impression: %s" % impression
		except Exception:
			print "Error with Impression"

		self.ad = ad

	def return_json(self):
		return self.ad

	def return_html(self):
		try:
			return self.ad.json()['ads']['ad'][0]['html']
		except Exception:
			return False

	def return_text(self):
		try:
			impression = self.ad.json()['ads']['ad'][0]['creative'][0]['tracking']['impression']
			click = self.ad.json()['ads']['ad'][0]['creative'][0]['tracking']['click']
			alt = self.ad.json()['ads']['ad'][0]['creative'][0]['alt']
			target = self.ad.json()['ads']['ad'][0]['creative'][0]['target']
			if target == "mxit":
				return '<img src="%s" /><a href="%s">%s</a> ' % (impression, click, alt)
			else:
				return '<img src="%s" /><a href="%s" onclick="window.open(this.href); return false;" >%s</a>' % (impression, click, alt)
		except Exception:
			return False

	def return_image(self):
		try:
			impression = self.ad.json()['ads']['ad'][0]['creative'][0]['tracking']['impression']
			media = self.ad.json()['ads']['ad'][0]['creative'][0]['media']
			click = self.ad.json()['ads']['ad'][0]['creative'][0]['tracking']['click']
			target = self.ad.json()['ads']['ad'][0]['creative'][0]['target']
			if target == "mxit":
				return '<a href="%s"><img src="%s" /><img src="%s" /></a>' % (click, media, impression)
			else:
				return '<a href="%s" onclick="window.open(this.href); return false;" ><img src="%s" /><img src="%s" /></a>' % (click, media, impression)
		except Exception:
			return False

if __name__ == "__main__":
	pass
	#print Shink("336971",[],"197.80.128.34").return_image()