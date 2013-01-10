#!/usr/bin/python
# Flask imports
from flask import Flask, render_template, request, redirect, url_for, session
# Database imports
from flask_sqlalchemy import SQLAlchemy
# Python imports
import random, sys

# Added extras!


# Mxit Analytics
from functools import wraps
from mxit_ga import MxitGa
from flask import request
def track_page(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		ga = MxitGa('UA-35740588-1')
		ga.track_page(request.headers, request.remote_addr, request.host, request.path, request.query_string)
		return f(*args, **kwargs)
	return decorated_function




# Init app object
app = Flask(__name__)
# Config

sys.path.insert(0,'/users/brad/apps/isonka/')
# ^AWESOME, but only necessary for local ffs
app.config.from_object("config")
db = SQLAlchemy(app)

import requests
from models import *
# Extra requests
@app.teardown_request
def teardown_request(exception):
	db.session.remove()

# Testing grounds
@app.route('/test')
def testy():
	#ua = request.headers['X-Device-User-Agent']
	#r = requests.get('http://ox-d.shinka.sh/ma/1.0/arj?auid=313837&c.device='+ua)
	#g = 'http://ox-d.shinka.sh/ma/1.0/arj?auid=313837&c.device='+ua
	shinks()
	return render_template('test.html',
	                       track = params['track'],
	                       img = params['img'],
	                       href = params['href'],
	                       alt = params['alt']
	                       )


# Login screen
@app.route('/')
@track_page
def login():

	if "X-Mxit-USERID-R" in request.headers:
		userID = request.headers['X-Mxit-USERID-R']
		name = request.headers['X-Mxit-Nick']
		ua = request.headers['X-Device-User-Agent']
	else:
		userID = 1
		name = 'brad'
		ua = 'MANdroid'
	player = Player.query.filter_by(username=userID).first()

	if not player:
		new = Player(userID,0,0,name)
		db.session.add(new)
		db.session.commit()



	return render_template('intro.html',
	                       name = name,
	                       ua = ua,
	                       player = player
	                       )



# Game screen
@app.route('/play')
@track_page
def play():
	# Sort out Isonka logic
	userID = request.headers['X-Mxit-USERID-R']
	name = request.headers['X-Mxit-Nick']
	player = Player.query.filter_by(username=userID).first()

	if not player:
		return redirect(url_for('login'))
	computer_choice = random.randrange(0,3)
	computer_weapon = ['ROCK','PAPER','SCISSORS']
	# Identify who's playing
	powerups = player.powerups
	# Parse GET data
	if request.args:
		player_choice = int(request.args['choice'])
		player_weapon = request.args['weapon']
		winning = player_choice - computer_choice
		# 1 or -2 means user wins
		# -1 or 2 means user loses
		# 0 means its a draw
		result = 'You '

		if powerups > 0:
			player.powerups -= 1
			db.session.commit()
			if winning == 1 or winning == -2:
				player.score += 2
				result += 'win'
			elif winning == -1 or winning == 2:
				result += 'lose'
			else:
				player.score += 1
				result += 'drew'
			"""DRAWWWWW"""
		else:
			if winning == 1 or winning == -2:
				player.score += 1
				result += 'won!'
			elif winning == -1 or winning == 2:
				player.score += -1
				result += 'lost.'
			else:
				result += 'drew.'
			"""DRAWWWWW"""

		db.session.commit()
		# Gameplay add-ons
		powerups = player.powerups
		total = player.score
		# ^This must be after commit to give correct score.
		# Therefore will be repeated again in else statement
		return render_template('index.html',
		                       result = result, # Win or lose etc
		                       computer = computer_weapon[computer_choice],
		                       user = player_weapon,
		                       total = total, # Total score
		                       powerups = powerups,
		                       userID = userID,  # Remove before deploy
		                       name = name
		                       )
		# ^THIS isn't finished, the result that is added must
		# be contingent on whether powerups are available or not
	else :
		result = 'Choose your weapon'
		powerups = player.powerups
		total = player.score
		return render_template('index.html',
		                       result = result,
		                       total = total,
		                       powerups = powerups,
		                       )
# Out for now
"""
@app.route('/reset')
@track_page
def reset():
	userID = request.headers['X-Mxit-USERID-R']
	player = Player.query.filter_by(username=userID).first()
	if not player:
		return redirect(url_for('login'))
	player.score = 0
	db.session.commit()
	return render_template('reset.html')
"""

@app.route('/powerup')
@track_page
def powerup():
	userID = request.headers['X-Mxit-USERID-R']
	player = Player.query.filter_by(username=userID).first()
	ua = request.headers['X-Device-User-Agent']
	if not player:
		return redirect(url_for('login'))
	player.powerups += 10
	db.session.commit()
	return render_template('powerup.html',
	                       ua = ua
	                       )

@app.route('/leaderboard')
@track_page
def leaderboard():
	from urllib import unquote
	import re
	players = Player.query.order_by('score desc').limit(10)
	#ua = request.headers['X-Device-User-Agent']
	listy = {}
	expr = r'#([a-fA-F0-9]{6}|[a-fA-F0-9]{3})'
	span_out = ''
	def convert(matchobj):
		output = '</span><span style="color: ' +	matchobj.group() + ';">'
		return output

	for instance in players:
		span_in = unquote(instance.name) # Get name, and unquote
		awesome = re.sub(expr, convert, span_in) # Replace and add spans
		listy[awesome] = instance.score
	import operator
	sorted_listy = sorted(listy.iteritems(), key = operator.itemgetter(1), reverse = True)
	return render_template('leaderboard.html',
	                       listy = sorted_listy
	                       )

@app.route('/shutdown')
def shutdown_server():
	func = request.environ.get('werkzeug.server.shutdown')
	if func is None:
			raise RuntimeError('Not running with the Werkzeug Server')
	func()




if __name__ == '__main__':
	app.run()
