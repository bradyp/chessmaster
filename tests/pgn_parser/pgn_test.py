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
    pgn_game = pgn.PGNGame()

    pgn_game.loads(pgn_text)
    pgn_game.dumps(pgn_game)
    
    print pgn_game.json()
    #if len(pgn_game.moves) == 2*len(pgn_game.json()):
    #  print pgn_game.moves
    #  print pgn_game.json()

##################################################
# Main

if __name__ == '__main__':
    games = pre_parse(sys.argv[1])
    for game in games:
      try:
        print_test(game)
      except AttributeError:#AtttributeError:
        continue
