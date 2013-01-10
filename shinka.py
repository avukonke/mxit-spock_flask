#!/usr/bin/python
from flask import request
import requests

class Shink(object):
	def __init__(self, ua):
		ad = requests.get('http://ox-d.shinka.sh/ma/1.0/arj?auid=313837').json # To serve diverse ads
		self.ad = ad['ads']['ad'][0]['creative'][0]

	def width(self):
		return self.ad['width']

	def height(self):
		return self.ad['height']

	def alt(self):
		return self.ad['alt']

	def media(self):
		return self.ad['media']

	def impression(self):
		return self.ad['tracking']['impression']

	def click(self):
		return self.ad['tracking']['click']


