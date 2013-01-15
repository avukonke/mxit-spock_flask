from random import randrange

def number_to_name(number):
  if(number == 0):
    result = 'rock'
  elif(number == 1):
    result = 'Spock'
  elif(number == 2):
    result = 'paper'
  elif(number == 3):
    result = 'lizard'
  elif(number == 4):
    result = 'scissors'
  return result

def name_to_number(name):
  if(name == 'rock'):
    result = 0
  elif(name == 'spock'):
    result = 1
  elif(name == 'paper'):
    result = 2
  elif(name == 'lizard'):
    result = 3
  elif(name == 'scissors'):
    result = 4
  return result

def rpsls(name):
  player_number = name_to_number(name)
  comp_number = randrange(0, 5)
  if player_number == comp_number:
  	return [2, comp_number] # Draw
  elif (comp_number + 1) % 5 == player_number:
    return [1, comp_number] # Player wins
  elif (comp_number + 2) % 5 == player_number:
    return [1, comp_number] # Player wins
  else:
    return [0, comp_number] # Player loses