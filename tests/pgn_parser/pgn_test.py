#!/usr/bin/python

##################################################
# Imports

import pgn_parser as pgn
import sys
import re

##################################################
# Classes & Methods

class History(object):
    """
    Records the history of all the moves done in each game.
    """
    def __init__(self):
        """
        Initialzie class variables
        """
        # Parsed game data
        self.game_data = []
        # State history of each game in 'game_data'
        self.all_states = []
        # Current game board state
        self.state = []


class Game(object):
    """
    This is the global game class which contains all game data.
    """
    def __init__(self):
        """
        Initialize class variables.
        """
        # record game histories
        self.games = History()
        # no piece exists
        self.invalid = '   '
        # board file mapping
        self.mapper = {'a': 1,
                       'b': 2,
                       'c': 3,
                       'd': 4,
                       'e': 5,
                       'f': 6,
                       'g': 7,
                       'h': 8
                       }

    def get_loc(self, move):
        """
        Get the location of a piece given a move on the board.
        """
        return self.mapper[move[-2]] + (8 - int(move[-1])) * 8

    def pretty_print_board(self, board):
        """
        Pretty print the current board state to the console.
        """
        horizontal = [' a ', ' b ', ' c ', ' d ', ' e ', ' f ', ' g ', ' h ']
        vertical = [8, 7, 6, 5, 4, 3, 2, 1]
        print '\n'
        print ' \t', horizontal, '\n'
        for i in xrange(8):
            print vertical[i], '\t', board[i * 8: (i + 1) * 8], (i + 1) * 8

    def pre_parse(self, filename):
        """
        Preparse the input file(s) to split the games using a '@' symbol.
        """
        f = open(filename)
        raw = f.read()
        subbed = re.sub('1-0\s', '1-0@', raw)
        subbed = re.sub('1/2-1/2\s', '1/2-1/2@', subbed)
        subbed = re.sub('0-1\s', '0-1@', subbed)
        self.games.game_data = subbed.split('@')

    def update_board(self, player, move):
        """
        Updates the current board state depending on the player and move
        that's being played.
        """
        # Remove useless symbols
        move = move.replace('+', '')
        move = move.replace('!', '')
        move = move.replace('?', '')
        move = move.replace('#', '')
        # Note, we will keep the '=' symbol indicating pawn promotion

        # If any unknown symbols still appear, throw an exception
        error = re.match('^[\w]+$', move)
        if(error is not None):
            if(error.group() != move):
                raise Exception('Unknown symbol(s) detected in (%s)' % move)

        # Special Moves require identifiers
        # Castling Queen-side
        if('O-O-O' in move):
            move = ('O-O-O', 59, 60)  # (king,rook)
            return None

        # Castling King-side
        elif('O-O' in move):
            move = ('O-O', 63, 62)  # (king,rook)
            return None

        # Normal Moves require that we base updates on piece movement rules
        # A normal move has been made, identify the piece's new location
        newloc = self.get_loc(move)

        # Pawn is being moved
        if(move[0] in self.mapper.keys()):
            oldloc = self.mapper[move[0]]
            if(player == 'W'):
                oldloc += (int(move[-1]) + 2) * 8 # modify to handle all jumps
            else:
                oldloc += (int(move[-1]) - 1) * 8
            print '\noldloc =', oldloc, '=', self.games.state[oldloc]
            print 'newloc =', newloc, '=', self.games.state[newloc]
            self.pretty_print_board(self.games.state)
            self.games.state[newloc] = self.games.state[oldloc]
            self.games.state[oldloc] = self.invalid
            self.pretty_print_board(self.games.state)
            exit() #TODO :: FIX THIS!

        # Rook is being moved
        elif(move[0] == 'R'):
            pass #TODO

        # Knight is being moved
        elif(move[0] == 'N'):
            pass #TODO

        # Bishop is being moved
        elif(move[0] == 'B'):
            pass #TODO

        # Queen is being moved
        elif(move[0] == 'Q'):
            pass #TODO

        # King is being moved
        elif(move[0] == 'K'):
            pass #TODO

        # Something went wrong
        else:
            raise Exception("Invalid move detected (%s)" % move)

        # Return the piece's new location
        return newloc

    def new_state(self, player, turn, move):
        """
        """
        print '--------------------------------------------'
        print 'player = ', player
        print 'turn = ', turn
        print 'move = ', move
        try:
            print 'elem = ', self.update_board(player, move)
            exit()
        except Exception, e:
            print '\n\nException caught: %s' % e
            exit()
        print '--------------------------------------------'
        return self.games.state

    def process_games(self, pgn_text):
        """
        Process each game's pgn_text to record the piece locations for
        every turn.
        """
        # Load the game data
        pgn_parser = pgn.PGNParser()
        pgn_parser.loads(pgn_text)
        pgn_parser.dumps(pgn_parser)

        # Process the move list to get in the form: (turn#, (white,black))
        move_list = map(lambda d: (d[0], d[1].split()),
                        pgn_parser.json().items())

        # Initial Board state for kicking off the game
        init = ['br1', 'bn1', 'bb1', 'bQQ', 'bKK', 'bb2', 'bn2', 'br2',
                'bp1', 'bp2', 'bp3', 'bp4', 'bp5', 'bp6', 'bp7', 'bp8',
                '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ',
                '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ',
                '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ',
                '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ',
                'wp1', 'wp2', 'wp3', 'wp4', 'wp5', 'wp6', 'wp7', 'wp8',
                'wr1', 'wn1', 'wb1', 'wQQ', 'wKK', 'wb2', 'wn2', 'wr2'
                ]
        self.games.state = init

        # For each (turn,move) in the game, record the board state
        for turn, moves in move_list:
            #Endgame detected, return
            if(len(moves) == 1):
                break

            # Update for white's turn
            self.games.all_states.append(self.new_state('W', turn, moves[0]))

            # Update for black's turn
            self.games.all_states.append(self.new_state('B', turn, moves[1]))

##################################################
# Main

if __name__ == '__main__':
    controller = Game()
    controller.pre_parse(sys.argv[1])
    for game in controller.games.game_data:
        try:
            controller.process_games(game)
        except AttributeError,e:  # AtttributeError:
            print '\n\nAttribute Exception caught (%s)' % e
            exit()
            #continue

