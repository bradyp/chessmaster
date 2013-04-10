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
  subbed = re.sub('1-0\s','1-0@',raw)
  subbed = re.sub('1/2-1/2\s','1/2-1/2@',subbed)
  subbed = re.sub('0-1\s','0-1@',subbed)
  output = subbed.split('@')
  return output
  pass

def print_test(pgn_text):
    """
    """
    #pgn_text = open(filename).read()
    pgn_game = pgn.PGNGame()

    #print pgn_game.loads(pgn_text)  # Returns a list of PGNGame
    #print '\n'
    #print pgn_game.dumps(pgn_game)  # Returns a string with a pgn game
    #print '\n'
    pgn_game.loads(pgn_text)
    pgn_game.dumps(pgn_game)
#    pgn_game.print_moves()

##################################################
# Main

if __name__ == '__main__':
    games = pre_parse(sys.argv[1])
    i=1
    print len(games)
    for game in games:
      try:
        print_test(game)
        print i
        i += 1
      except AttributeError:#AtttributeError:
        continue
