#!/usr/bin/python
import mechanize

class GetMyIP():
	def __init__(self):
		br = mechanize.Browser()
		br.set_handle_equiv(True)
		#br.set_handle_gzip(True)
		br.set_handle_redirect(True)
		br.set_handle_referer(True)
		br.set_handle_robots(False)
		self.br = br

	def get_my_ip(self):

		result = self.br.open("http://ifconfig.me/all.json")
		result = result.read()
		import simplejson as json
		json_file = json.loads(result) 
		return json_file["ip_addr"]

		
if __name__ == "__main__":
	getIP = GetMyIP()
	print getIP.get_my_ip()