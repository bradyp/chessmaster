#!/usr/bin/python

##################################################
# Imports

import pgn_parser as pgn
import sys
##################################################
# Tester
def pre_parse(filename):
  pass

def print_test(filename):
    """
    """
    pgn_text = open(filename).read()
    pgn_game = pgn.PGNGame()

    print pgn_game.loads(pgn_text)  # Returns a list of PGNGame
    print '\n'
    print pgn_game.dumps(pgn_game)  # Returns a string with a pgn game
    print '\n'
    pgn_game.print_moves()

##################################################
# Main

#print_test('example.pgn')
pre-parse(sys.argv[1])
