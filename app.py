#!/usr/bin/python
from flask import Flask, render_template, request, redirect, url_for
from models import MxitUser, session
from spock import rpsls, number_to_name
from functools import wraps
from mxit_ga import MxitGa

app = Flask(__name__)
app.config.from_object("config")

def track_page(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		ga = MxitGa('UA-35740588-1')
		ga.track_page(request.headers, request.remote_addr, request.host, request.path, request.query_string)
		return f(*args, **kwargs)
	return decorated_function

#sys.path.insert(0,'/users/brad/apps/isonka/')

@app.route('/')
@track_page
def index():

	if "X-Mxit-USERID-R" not in request.headers:
		mxit_id = 1
		nick = 'brad'
		ua = 'MANdroid'
	else:
		mxit_id = request.headers['X-Mxit-USERID-R']
		nick = request.headers['X-Mxit-Nick']
		ua = request.headers['X-Device-User-Agent']

	user = session.query(MxitUser).filter_by(mxit_id=mxit_id).first()

	if not user:
		user = MxitUser(mxit_id, nick)
		session.add(user)
		session.commit()

	return render_template('index.html',
												nick=nick,
												ua=ua,
												user=user
												)


# Game screen
@app.route('/play')
@track_page
def play():
	if "X-Mxit-USERID-R" not in request.headers:
		mxit_id = 1
		nick = 'brad'
	else:
		mxit_id = request.headers['X-Mxit-USERID-R']
		nick = request.headers['X-Mxit-Nick']

	user = session.query(MxitUser).filter_by(mxit_id=mxit_id).first()
	if not user:
		return redirect(url_for('index'))

	if request.args:
		user_choice = request.args['choice']
		game = rpsls(user_choice)
		if game[0] == 0:
			result = "You lose."
			user.points -= 1
		elif game[0] == 1:
			result = "You win!"
			user.points += 1
		else:
			result = "It's a draw."
		user.games_played += 1
		session.commit()
		message = ''
		if user.games_played % 10 == 0:
			user.points += 5
			session.commit()
			message = 'You\'ve played %s games - you get 5 bonus points!' % str(user.games_played)
		return render_template('play.html',
													result=result, # Win or lose etc
													user_weapon=user_choice,
													computer_weapon=number_to_name(game[1]),
													total=user.points, # Total score
													mxit_id=mxit_id,  # Remove before deploy
													nick=nick,
													games_played=user.games_played,
													message=message,
													)
	else:
		result = 'Choose your weapon'
		total = user.points
		return render_template('play.html',
													result=result,
													total=total,
													)

@app.route('/rules')
@track_page
def powerup():
	return render_template('rules.html')

@app.route('/leaderboard')
@track_page
def leaderboard():
	from urllib import unquote
	import re
	players = session.query(MxitUser).order_by('points desc').limit(10)
	#ua = request.headers['X-Device-User-Agent']
	listy = {}
	expr = r'#([a-fA-F0-9]{6}|[a-fA-F0-9]{3})'

	def convert(matchobj):
		output = '</span><span style="color: ' + matchobj.group() + ';">'
		return output

	for instance in players:
		span_in = unquote(instance.mxit_nick) # Get name, and unquote
		name = re.sub(expr, convert, span_in).decode('ascii') # Replace and add spans
		listy[name] = instance.points
	import operator
	sorted_listy = sorted(listy.iteritems(), key=operator.itemgetter(1), reverse=True)
	return render_template('leaderboard.html',
												listy=sorted_listy
												)


if __name__ == '__main__':
	app.run()
