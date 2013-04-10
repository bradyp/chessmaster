#!/usr/bin/python

##################################################
# Imports

import pgn_parser as pgn
import sys
import re

##################################################
# Tester
def pre_parse(filename):
  f = open(filename)
  raw = f.read()
  subbed = re.sub('1-0','1-0@',raw)
  subbed = re.sub('1/2-1/2','1/2-1/2@',subbed)
  subbed = re.sub('0-1','0-1@',subbed)
  output = subbed.split('@')
  return output
  pass

def print_test(pgn_text):
    """
    """
    #pgn_text = open(filename).read()
    pgn_game = pgn.PGNGame()

    print pgn_game.loads(pgn_text)  # Returns a list of PGNGame
    print '\n'
    print pgn_game.dumps(pgn_game)  # Returns a string with a pgn game
    print '\n'
    pgn_game.print_moves()

##################################################
# Main

games = pre_parse(sys.argv[1])
print games
for game in games:
  print_test(game)
#print_test('example.pgn')
