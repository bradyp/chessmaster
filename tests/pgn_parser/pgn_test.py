#!/usr/bin/python

##################################################
# Imports

import os
import pgn_parser as pgn
import copy
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
        Initialize class variables.
        """
        # Parsed game data
        self.game_data = []
        # State history of a game in 'game_data'
        self.all_states = []


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
        # Current game board state
        self.state = []
        # no piece exists
        self.empty_tile = ''
        # board file mapping
        self.mapper = {'a': 0,
                       'b': 1,
                       'c': 2,
                       'd': 3,
                       'e': 4,
                       'f': 5,
                       'g': 6,
                       'h': 7
                       }

    def isInteger(self, symbol):
        try:
            int(symbol)
            return True
        except ValueError:
            return False

    def getRow(self, index):
        """
        Find the row of a given tile.
        """
        for i in xrange(0, 64, 8):
            if(index in xrange(i, (i + 1) * 8)):
                return i

    def isInColumn(self, col, index):
        """
        Is the index in column col?
        """
        # Return true if the index is in the given column
        if(type(col) != type(0)):
            return (index in xrange(self.mapper[col], 65, 8))
        else:
            return (index in xrange(col, 65, 8))

    def isInRow(self, row, index):
        """
        Is the idnex in row 'row'?
        """
        # return true if the index is in the given row
        return (index in xrange(8*(8-row),8*(8-row+1)))

    def inBorder(self, curIndex, nextIndex):
        """
        Used to avoid twisting around the board.
        """
        # Left or right border of the game board
        if(curIndex in range(0, 65, 8) and nextIndex in range(7, 65, 8)):
            return True
        if(nextIndex in range(0, 65, 8) and curIndex in range(7, 65, 8)):
            return True
        # Top or bottom border of the game board
        if(nextIndex > 63 or nextIndex < 0):
            return True
        # Inner part of the game board
        return False

    def getLoc(self, row, column):
        """
        Get the location of a piece given a move on the board.
        """
        return ((8 - int(row)) * 8) + self.mapper[column]

    def prettyPrintBoard(self, board):
        """
        Debug method.
        Pretty print the current board state to the console.
        """
        horizontal = [' a ', ' b ', ' c ', ' d ', ' e ', ' f ', ' g ', ' h ']
        vertical = [8, 7, 6, 5, 4, 3, 2, 1]
        print '\n \t', horizontal, '\n'
        for i in xrange(8):
            print vertical[i], '\t', board[i * 8: (i + 1) * 8], (i + 1) * 8 - 1
        print '\n'

    def preParse(self, filename):
        """
        Preparse the input file(s) to split the games using a '@' symbol.
        """
        f = open(filename)
        raw = f.read()
        subbed = re.sub('1-0\s', '1-0@', raw)
        subbed = re.sub('1/2-1/2\s', '1/2-1/2@', subbed)
        subbed = re.sub('0-1\s', '0-1@', subbed)
        self.games.game_data = subbed.split('@')

    def updateBoard(self, player, newmove):
        """
        Updates the current board state depending on the player and move
        that's being played.
        """
        # Create copy of the new move
        move = newmove

        # Display current board state
        #self.prettyPrintBoard(self.state)

        # Remove useless symbols
        move = move.replace('+', '')
        move = move.replace('!', '')
        move = move.replace('?', '')
        move = move.replace('#', '')
        # Note, we will keep the '=' symbol indicating pawn promotion

        # Special Moves require identifiers
        # Castling Queen-side
        if('O-O-O' in move):
            if(player == 'B'):
                self.state[0] = self.empty_tile
                self.state[4] = self.empty_tile
                self.state[2] = 'bKK'
                self.state[3] = 'bR1'
            else:
                self.state[56] = self.empty_tile
                self.state[60] = self.empty_tile
                self.state[58] = 'wKK'
                self.state[59] = 'wR1'
            return 'O-O-O'

        # Castling King-side
        elif('O-O' in move):
            if(player == 'B'):
                self.state[4] = self.empty_tile
                self.state[7] = self.empty_tile
                self.state[6] = 'bKK'
                self.state[5] = 'bR2'
            else:
                self.state[60] = self.empty_tile
                self.state[63] = self.empty_tile
                self.state[62] = 'wKK'
                self.state[61] = 'wR2'
            return 'O-O'

        # Normal Moves require that we base updates on piece movement rules
        # A normal move has been made, identify the piece's new location
        if('=' not in move):
            newloc = self.getLoc(move[-1], move[-2])
        else:
            newloc = self.getLoc(move[-3], move[-4])

        # Pawn is being moved
        if(move[0] in self.mapper.keys()):
            #print 'Moving Pawn'
            # If pawn is not capturing, move it
            if('x' not in move):
                if(player == 'W'):
                    l1 = newloc + 8 * 1
                    l2 = newloc + 8 * 2
                    if(re.search(r'wP\d', self.state[l1])):
                        self.state[newloc] = self.state[l1]
                        self.state[l1] = self.empty_tile
                    elif(re.search(r'wP\d', self.state[l2])):
                        self.state[newloc] = self.state[l2]
                        self.state[l2] = self.empty_tile
                else:
                    l1 = newloc - 8 * 1
                    l2 = newloc - 8 * 2
                    if(re.search(r'bP\d', self.state[l1])):
                        self.state[newloc] = self.state[l1]
                        self.state[l1] = self.empty_tile
                    elif(re.search(r'bP\d', self.state[l2])):
                        self.state[newloc] = self.state[l2]
                        self.state[l2] = self.empty_tile

            # Handle capturing
            else:
                row, col = None, None
                oldloc = None
                enpassante = None
                if('=' in move):
                    col, row = -4, -3
                else:
                    col, row = -2, -1
                oldloc = self.getLoc(move[row], move[col])

                if(player == 'W'):
                    oldloc += 8
                else:
                    oldloc -= 8
                if(self.isInColumn(move[0], newloc-1)):
                    oldloc -= 1
                else:
                    oldloc += 1

                if(self.state[newloc] == self.empty_tile):
                    if('P' in self.state[oldloc-1] and
                        self.isInColumn(move[col],oldloc-1)):
                        enpassante = oldloc - 1;
                    elif('P' in self.state[oldloc+1] and
                        self.isInColumn(move[col],oldloc+1)):
                        enpassante = oldloc + 1;

                self.state[newloc] = self.state[oldloc]
                self.state[oldloc] = self.empty_tile
                if(enpassante is not None):
                    self.state[enpassante] = self.empty_tile

            # Handle pawn promotion
            if('=' in move):
                if(player == 'W'):
                    self.state[newloc] = 'w'
                else:
                    self.state[newloc] = 'b'
                if('R' in move):
                    self.state[newloc] += 'RR'
                elif('N' in move):
                    self.state[newloc] += 'NN'
                elif('B' in move):
                    self.state[newloc] += 'BB'
                elif('Q' in move):
                    self.state[newloc] += 'QQ'
                else:
                    raise Exception('Unknown premotion %s' % move)

        # Knight is being moved
        elif(move[0] == 'N'):
            #print 'Moving Knight'
            move = move.replace('x', '')
            locs = [newloc - 8 * 2 + 1,
                    newloc - 8 + 2,
                    newloc - 8 - 2,
                    newloc - 8 * 2 - 1,
                    newloc + 8 + 2,
                    newloc + 8 * 2 + 1,
                    newloc + 8 * 2 - 1,
                    newloc + 8 - 2,
                    ]
            locs2 = []

            # Remove artifact knight locations due to 1D representation
            if('c' != move[-2] and
               'd' != move[-2] and
               'e' != move[-2] and
               'f' != move[-2]):
                if('a' == move[-2]):
                    locs.pop(locs.index(newloc + 8 * 2 - 1))
                    locs.pop(locs.index(newloc + 8 - 2))
                    locs.pop(locs.index(newloc - 8 - 2))
                    locs.pop(locs.index(newloc - 8 * 2 - 1))
                elif('b' == move[-2]):
                    locs.pop(locs.index(newloc + 8 - 2))
                    locs.pop(locs.index(newloc - 8 - 2))
                elif('g' == move[-2]):
                    locs.pop(locs.index(newloc + 8 + 2))
                    locs.pop(locs.index(newloc - 8 + 2))
                elif('h' == move[-2]):
                    locs.pop(locs.index(newloc + 8 * 2 + 1))
                    locs.pop(locs.index(newloc + 8 + 2))
                    locs.pop(locs.index(newloc - 8 + 2))
                    locs.pop(locs.index(newloc - 8 * 2 + 1))
                else:
                    msg = 'Unknown file for knight move (%s)' % move[-2]
                    raise Exception(msg)

            # Gather possible previous knight locations
            for elem in locs:
                if(elem <= 63 and elem >= 0):
                    if(player == 'W' and 'wN' in self.state[elem]):
                        locs2.append(elem)
                    elif(player == 'B' and 'bN' in self.state[elem]):
                        locs2.append(elem)

            # One knight is move/capturing
            if(len(move) == 3):
                self.state[newloc] = self.state[locs2[0]]
                self.state[locs2[0]] = self.empty_tile

            # Two or more knights on the same row
            #TODO: Allowing errors in knight locations when
            #      there exist more than two knights due to
            #      time constraints.
            #FIX LATER!
            elif(len(move) == 4):
                self.isInteger(move[1])
                oldloc = None
                if(self.isInteger(move[1])):
                    for loc in locs2:
                        if(self.isInRow(int(move[1]),loc)):
                            oldloc = loc
                else:
                    for loc in locs2:
                        if(self.isInColumn(move[1],loc)):
                            oldloc = loc
                            break
                self.state[newloc] = self.state[oldloc]
                self.state[oldloc] = self.empty_tile

            # Two knights on the same file
            elif(len(move) == 5):
                oldloc = self.getLoc(move[1], move[2])
                self.state[newloc] = self.state[oldloc]
                self.state[oldloc] = self.empty_tile

            else:
                raise Exception('Unknown knight move detected: (%s)' % move)

        # Rook is being moved
        #TODO: Allowing errors in rook locations when
        #      there exist more than two rooks due to
        #      time constraints.
        #FIX LATER!
        elif(move[0] == 'R'):
            #print 'Moving Rook'
            move = move.replace('x', '')
            locs = []
            left, right, top, bottom = True, True, True, True
            lmove, rmove = newloc, newloc
            tmove, bmove = newloc, newloc

            # Find all possible rook locations along the
            # new locations rank and file.
            while(left or right or top or bottom):
                # Find all possible positions to the left
                if(left):
                    if(self.inBorder(lmove, lmove - 1)):
                        left = False
                    else:
                        if(self.state[lmove - 1] == self.empty_tile):
                            lmove -= 1
                        elif('R' in self.state[lmove-1]):
                            lmove -= 1
                            locs.append(lmove)
                            left = False
                        else:
                            left = False

                # Find all possible positions to the right
                if(right):
                    if(self.inBorder(rmove, rmove + 1)):
                        right = False
                    else:
                        if(self.state[rmove + 1] == self.empty_tile):
                            rmove += 1
                        elif('R' in self.state[rmove + 1]):
                            rmove += 1
                            locs.append(rmove)
                            right = False
                        else:
                            right = False
                # Find all possible positions to the top
                if(top):
                    if(self.inBorder(tmove, tmove - 8)):
                        top = False
                    else:
                        if(self.state[tmove - 8] == self.empty_tile):
                            tmove -= 8
                        elif('R' in self.state[tmove - 8]):
                            tmove -= 8
                            locs.append(tmove)
                            top = False
                        else:
                            top = False
                # Find all possible positions to the bottom
                if(bottom):
                    if(self.inBorder(bmove, bmove + 8)):
                        bottom = False
                    else:
                        if(self.state[bmove + 8] == self.empty_tile):
                            bmove += 8
                        elif('R' in self.state[bmove + 8]):
                            bmove += 8
                            locs.append(bmove)
                            bottom = False
                        else:
                            bottom = False

            if(len(move) == 3):
                oldloc = None
                for loc in locs:
                    if(player == 'W' and 'wR' in self.state[loc]):
                        oldloc = loc
                        break
                    elif(player == 'B' and 'bR' in self.state[loc]):
                        oldloc = loc
                        break
                if(oldloc is None):
                    raise Exception('Could not find rook for move1: %s' % move)
                else:
                    self.state[newloc] = self.state[oldloc]
                    self.state[oldloc] = self.empty_tile
            elif(len(move) == 4):
                oldloc = None
                if(self.isInteger(move[1])):
                    for loc in locs:
                        if(player == 'W' and
                            'wR' in self.state[loc] and
                            self.isInRow(int(move[1]), loc)):
                            oldloc = loc
                            break
                        elif(player == 'B' and
                            'bR' in self.state[loc] and
                            self.isInRow(int(move[1]), loc)):
                            oldloc = loc
                            break
                else:
                    for loc in locs:
                        if(player == 'W' and
                            'wR' in self.state[loc] and
                            self.isInColumn(move[1], loc)):
                            oldloc = loc
                            break
                        elif(player == 'B' and
                            'bR' in self.state[loc] and
                            self.isInColumn(move[1], loc)):
                            oldloc = loc
                            break
                if(oldloc is None):
                    raise Exception('Could not find rook for move2: %s' % move)
                else:
                    self.state[newloc] = self.state[oldloc]
                    self.state[oldloc] = self.empty_tile
            elif(len(move) == 5):
                oldloc = self.getLoc(move[1], move[2])
                self.state[newloc] = self.state[oldloc]
                self.state[oldloc] = self.empty_tile

        # Bishop is being moved
        #TODO: Allowing errors in bishop locations when
        #      there exist more than two bishop due to
        #      time constraints.
        #FIX LATER!
        elif(move[0] == 'B'):
            #print 'Moving Bishop'
            move = move.replace('x', '')
            locs = []
            lu, ru, ld, rd = True, True, True, True
            lumove, rumove = newloc, newloc
            ldmove, rdmove = newloc, newloc

            # Find all possible rook locations along the
            # new locations rank and file.
            while(lu or ru or ld or rd):
                # Find all possible positions to the upper-left diagonal
                if(lu):
                    if(self.inBorder(lumove, lumove - 9)):
                        lu = False
                    else:
                        if(self.state[lumove - 9] == self.empty_tile):
                            lumove -= 9
                        elif('B' in self.state[lumove - 9]):
                            lumove -= 9
                            locs.append(lumove)
                            lu = False
                        else:
                            lu = False

                # Find all possible positions to the upper-right diagonal
                if(ru):
                    if(self.inBorder(rumove, rumove - 7)):
                        ru = False
                    else:
                        if(self.state[rumove - 7] == self.empty_tile):
                            rumove -= 7
                        elif('B' in self.state[rumove - 7]):
                            rumove -= 7
                            locs.append(rumove)
                            ru = False
                        else:
                            ru = False
                # Find all possible positions to the lower-left diagonal
                if(ld):
                    if(self.inBorder(ldmove, ldmove + 7)):
                        ld = False
                    else:
                      if(self.state[ldmove + 7] == self.empty_tile):
                          ldmove += 7
                      elif('B' in self.state[ldmove + 7]):
                          ldmove += 7
                          locs.append(ldmove)
                          ld = False
                      else:
                          ld = False
                # Find all possible positions to the lower-right diagonal
                if(rd):
                    if(self.inBorder(rdmove, rdmove + 9)):
                        rd = False
                    else:
                        if(self.state[rdmove + 9] == self.empty_tile):
                            rdmove += 9
                        elif('B' in self.state[rdmove + 9]):
                            rdmove += 9
                            locs.append(rdmove)
                            rd = False
                        else:
                            rd = False

            if(len(move) == 3):
                oldloc = None
                for loc in locs:
                    if(player == 'W' and 'wB' in self.state[loc]):
                        oldloc = loc
                        break
                    elif(player == 'B' and 'bB' in self.state[loc]):
                        oldloc = loc
                        break
                if(oldloc is None):
                    msg = 'Could not find bishop for move1: %s' % move
                    raise Exception(msg)
                else:
                    self.state[newloc] = self.state[oldloc]
                    self.state[oldloc] = self.empty_tile
            elif(len(move) == 4):
                oldloc = None
                if(self.isInteger(move[1])):
                    for loc in locs:
                        if(player == 'W' and
                            'wB' in self.state[loc] and
                            self.isInRow(int(move[1]), loc)):
                            oldloc = loc
                            break
                        elif(player == 'B' and
                            'bB' in self.state[loc] and
                            self.isInRow(int(move[1]), loc)):
                            oldloc = loc
                            break
                else:
                    for loc in locs:
                        if(player == 'W' and
                            'wB' in self.state[loc] and
                            self.isInColumn(move[1], loc)):
                            oldloc = loc
                            break
                        elif(player == 'B' and
                            'bB' in self.state[loc] and
                            self.isInColumn(move[1], loc)):
                            oldloc = loc
                            break
                if(oldloc is None):
                    msg = 'Could not find bishop for move2: %s' % move
                    raise Exception(msg)
                else:
                    self.state[newloc] = self.state[oldloc]
                    self.state[oldloc] = self.empty_tile
            elif(len(move) == 5):
                oldloc = self.getLoc(move[1], move[2])
                self.state[newloc] = self.state[oldloc]
                self.state[oldloc] = self.empty_tile

        # Queen is being moved
        elif(move[0] == 'Q'):
            #print 'Moving Queen'
            move = move.replace('x', '')
            locs = []

            left, right, top, bottom = True, True, True, True
            lu, ru, ld, rd = True, True, True, True

            lmove, rmove = newloc, newloc
            tmove, bmove = newloc, newloc
            lumove, rumove = newloc, newloc
            ldmove, rdmove = newloc, newloc

            # Find all possible rook locations along the
            # new locations rank and file.
            while(left or right or top or bottom or lu or ru or ld or rd):
                # Find all possible positions to the left
                if(left):
                    if(self.inBorder(lmove, lmove - 1)):
                        left = False
                    else:
                        if(self.state[lmove - 1] == self.empty_tile):
                            lmove -= 1
                        elif('Q' in self.state[lmove-1]):
                            lmove -= 1
                            locs.append(lmove)
                            left = False
                        else:
                            left = False

                # Find all possible positions to the right
                if(right):
                    if(self.inBorder(rmove, rmove + 1)):
                        right = False
                    else:
                        if(self.state[rmove + 1] == self.empty_tile):
                            rmove += 1
                        elif('Q' in self.state[rmove + 1]):
                            rmove += 1
                            locs.append(rmove)
                            right = False
                        else:
                            right = False
                # Find all possible positions to the top
                if(top):
                    if(self.inBorder(tmove, tmove - 8)):
                        top = False
                    else:
                        if(self.state[tmove - 8] == self.empty_tile):
                            tmove -= 8
                        elif('Q' in self.state[tmove - 8]):
                            tmove -= 8
                            locs.append(tmove)
                            top = False
                        else:
                            top = False
                # Find all possible positions to the bottom
                if(bottom):
                    if(self.inBorder(bmove, bmove + 8)):
                        bottom = False
                    else:
                        if(self.state[bmove + 8] == self.empty_tile):
                            bmove += 8
                        elif('Q' in self.state[bmove + 8]):
                            bmove += 8
                            locs.append(bmove)
                            bottom = False
                        else:
                            bottom = False
                # Find all possible positions to the upper-left diagonal
                if(lu):
                    if(self.inBorder(lumove, lumove - 9)):
                        lu = False
                    else:
                        if(self.state[lumove - 9] == self.empty_tile):
                            lumove -= 9
                        elif('Q' in self.state[lumove - 9]):
                            lumove -= 9
                            locs.append(lumove)
                            lu = False
                        else:
                            lu = False

                # Find all possible positions to the upper-right diagonal
                if(ru):
                    if(self.inBorder(rumove, rumove - 7)):
                        ru = False
                    else:
                        if(self.state[rumove - 7] == self.empty_tile):
                            rumove -= 7
                        elif('Q' in self.state[rumove - 7]):
                            rumove -= 7
                            locs.append(rumove)
                            ru = False
                        else:
                            ru = False
                # Find all possible positions to the lower-left diagonal
                if(ld):
                    if(self.inBorder(ldmove, ldmove + 7)):
                        ld = False
                    else:
                      if(self.state[ldmove + 7] == self.empty_tile):
                          ldmove += 7
                      elif('Q' in self.state[ldmove + 7]):
                          ldmove += 7
                          locs.append(ldmove)
                          ld = False
                      else:
                          ld = False
                # Find all possible positions to the lower-right diagonal
                if(rd):
                    if(self.inBorder(rdmove, rdmove + 9)):
                        rd = False
                    else:
                        if(self.state[rdmove + 9] == self.empty_tile):
                            rdmove += 9
                        elif('Q' in self.state[rdmove + 9]):
                            rdmove += 9
                            locs.append(rdmove)
                            rd = False
                        else:
                            rd = False

            if(len(move) >= 3):
                oldloc = None
                for loc in locs:
                    if(player == 'W' and 'wQ' in self.state[loc]):
                        oldloc = loc
                        break
                    elif(player == 'B' and 'bQ' in self.state[loc]):
                        oldloc = loc
                        break
                if(oldloc is None):
                    msg = 'Could not find queen for move1: %s' % move
                    raise Exception(msg)
                else:
                    self.state[newloc] = self.state[oldloc]
                    self.state[oldloc] = self.empty_tile
            elif(len(move) == 4):
                oldloc = None
                if(self.isInteger(move[1])):
                    for loc in locs:
                        if(player == 'W' and
                            'wQ' in self.state[loc]
                            and self.isInRow(int(move[1]), loc)):
                            oldloc = loc
                            break
                        if(player == 'B' and
                            'bQ' in self.state[loc]
                            and self.isInRow(int(move[1]), loc)):
                            oldloc = loc
                            break
                else:
                    for loc in locs:
                        if(player == 'W' and
                            'wQ' in self.state[loc]
                            and self.isInColumn(move[1], loc)):
                            oldloc = loc
                            break
                        if(player == 'B' and
                            'bQ' in self.state[loc]
                            and self.isInColumn(move[1], loc)):
                            oldloc = loc
                            break
                if(oldloc is None):
                    msg = 'Could not find queen for move2: %s' % move
                    raise Exception(msg)
                else:
                    self.state[newloc] = self.state[oldloc]
                    self.state[oldloc] = self.empty_tile
            elif(len(move) == 5):
                oldloc = self.getLoc(move[1], move[2])
                self.state[newloc] = self.state[oldloc]
                self.state[oldloc] = self.empty_tile

        # King is being moved
        elif(move[0] == 'K'):
            #print 'Moving King'
            move = move.replace('x', '')
            locs = []
            if(not self.inBorder(newloc, newloc - 8 - 1)):
                locs.append(newloc - 8 - 1)
            if(not self.inBorder(newloc, newloc - 8 - 0)):
                locs.append(newloc - 8 - 0)
            if(not self.inBorder(newloc, newloc - 8 + 1)):
                locs.append(newloc - 8 + 1)
            if(not self.inBorder(newloc, newloc - 1)):
                locs.append(newloc - 1)
            if(not self.inBorder(newloc, newloc + 1)):
                locs.append(newloc + 1)
            if(not self.inBorder(newloc, newloc + 8 - 1)):
                locs.append(newloc + 8 - 1)
            if(not self.inBorder(newloc, newloc + 8 + 0)):
                locs.append(newloc + 8 + 0)
            if(not self.inBorder(newloc, newloc + 8 + 1)):
                locs.append(newloc + 8 + 1)
            locs2 = []

            for elem in locs:
                if(elem <= 63 and elem >= 0):
                    locs2.append(self.state[elem])

            if(player == 'W' and 'wKK' in locs2):
                oldloc = locs[locs2.index('wKK')]
                self.state[newloc] = self.state[oldloc]
                self.state[oldloc] = self.empty_tile
            elif(player == 'B' and 'bKK' in locs2):
                oldloc = locs[locs2.index('bKK')]
                self.state[newloc] = self.state[oldloc]
                self.state[oldloc] = self.empty_tile
            else:
                msg = 'Could not find king for move: %s' % move
                raise Exception(msg)

        # Something went wrong
        else:
            raise Exception('Invalid move detected: (%s)' % move)

        # Display updated board state
        #self.prettyPrintBoard(self.state)

        # Return the piece's new location
        return newloc

    def new_state(self, player, turn, move):
        """
        Wrapper method for the updateBoard() method.
        """
        try:
            self.updateBoard(player, move)
        except Exception, e:
            #print 'Exception caught: %s' % e
            raise('Ignore game.')
        return self.state

    def process_games(self, pgn_text):
        """
        Process each game's pgn_text to record the piece locations for
        every turn.
        """
        # Load the game data
        parser = pgn.PGNParser()
        parser.loads(pgn_text)
        parser.dumps(parser)

        # Process the move list to get in the form: (turn#, (white,black))
        move_list = map(lambda d: (d[0], d[1].split()), parser.json().items())

        # Initial Board state for kicking off a game
        init = ['bR1', 'bN1', 'bB1', 'bQQ', 'bKK', 'bB2', 'bN2', 'bR2',
                'bP1', 'bP2', 'bP3', 'bP4', 'bP5', 'bP6', 'bP7', 'bP8',
                '', '', '', '', '', '', '', '',
                '', '', '', '', '', '', '', '',
                '', '', '', '', '', '', '', '',
                '', '', '', '', '', '', '', '',
                'wP1', 'wP2', 'wP3', 'wP4', 'wP5', 'wP6', 'wP7', 'wP8',
                'wR1', 'wN1', 'wB1', 'wQQ', 'wKK', 'wB2', 'wN2', 'wR2'
                ]
        self.state = init
        self.games.all_states.append(copy.deepcopy(self.state))

        # For each (turn,move) in the game, record the board state for turn, moves in move_list:
        outcome = None
        for turn,moves in move_list:
            #Endgame detected, return
            if(len(moves) == 1):
                outcome = moves[0]
                break

            # Update for white's turn
            self.new_state('W', turn, moves[0])
            self.games.all_states.append(copy.deepcopy(self.state))

            if('1-0' in moves[1] or
                '0-1' in moves[1] or
                '1/2-1/2' in moves[1]):
                outcome = moves[1]
                break

            # Update for black's turn
            self.new_state('B', turn, moves[1])
            self.games.all_states.append(copy.deepcopy(self.state))

        # Display final board state
        print '[',
        num_states = len(self.games.all_states)
        for i in xrange(num_states):
            print self.games.all_states[i],','
        if(outcome == '1-0'):
            outcome = 'w'
        elif(outcome == '0-1'):
            outcome = 'b'
        else:
            outcome = 't'
        print [outcome],']\n\n@\n'

        # Reset containers
        self.games.all_states = []
        self.state = []

##################################################
# Main

if __name__ == '__main__':
    controller = Game()
    controller.preParse(sys.argv[1])
    count = 0
    fails = 0
    for game in controller.games.game_data:
        try:
            controller.process_games(game)
            count += 1
        except Exception:  # AttributeError:
            fails += 1
            #print 'ERROR on game %d\n' % count
            continue

