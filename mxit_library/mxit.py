#!/usr/bin/python

#Include Brad's great REGEX pretty print MXit Nick code:

def pretty_nicknames(player_nick):
	"""	Pretty prints out a nickname.
		Input a nickname. (Str)
		Output a pretty printed nickname. (Str)
	"""
	import re
	expr = r'#([a-fA-F0-9]{6}|[a-fA-F0-9]{3})'
	def convert(matchobj):
		output = '</span><span style="color: ' +	matchobj.group() + ';">'
		return output

	return re.sub(expr, convert, player_nick) # Replace and add spans