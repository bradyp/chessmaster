"""
Notes:
http://stackoverflow.com/questions/1894269/convert-string-list-to-list-in-python (parsing file)

"""
import string
import ast, sys, copy
import ast, sys, copy
import simplejson as json

from collections import defaultdict

def readfile(filename):
    """
    INPUT:filename for processed data file containing board states deliminated with '@'
    OUTPUT:list of games where a game is a list of states where a state is a list of moves where a move is a character of the form color/piece/numerical identifier
    """
    f = open(filename)
    games = f.read().split('@')
    f.close()
    output = []
    id = ['A8','B8','C8','D8','E8','F8','G8','H8',
          'A7','B7','C7','D7','E7','F7','G7','H7',
          'A6','B6','C6','D6','E6','F6','G6','H6',
          'A5','B5','C5','D5','E5','F5','G5','H5',
          'A4','B4','C4','D4','E4','F4','G4','H4',
          'A3','B3','C3','D3','E3','F3','G3','H3',
          'A2','B2','C2','D2','E2','F2','G2','H2',
          'A1','B1','C1','D1','E1','F1','G1','H1',
          ]
    maxlen = 0
    minlen = 1e6
    for entry in games:
        try:
          game = ast.literal_eval(entry)
        except Exception, e:
          print 'Exception:',e
          print 'Error occurred on entry:',entry
          exit()
        refined_game = []
        for state in game:
            refined_game.append(dict(zip(id,state)))
            if len(refined_game[-1]) > maxlen:
                maxlen = len(refined_game[-1])
            if len(refined_game[-1]) < minlen:
                minlen = len(refined_game[-1])
        output.append(refined_game)

    print 'maxlen = ',maxlen
    print 'minlen = ',minlen
    return output

def count(games, piece):
    """
    INPUT: list of games where a game is a list of states where a state is a list of moves where a move is a character of the form color/piece/numerical identifier, and piece identifier
    OUTPUT: list states, each state is a dict with id for key and a dict for the value, the dict will have keys of unique pieceid and values of how many occured there
    NEW_OUTPUT:dictionary of states with ints for keys and dicts for values, the values

    Ex: output: {0:{A1:0,A2:0.03,...G8:0.05}, 1:{...}, ...}
    """
    #prepare
    record = defaultdict(float) #this is an instance of the lowest most
    longest = max([len(game) for game in games])-1
    print '---------------------------------------'
    print 'longest game for %s had %d turns.' % (piece,longest)
    print '---------------------------------------'
    output = {}
    helper = {}
    for i in range(longest):
        output[i] = copy.deepcopy(record)
        helper[i] = copy.deepcopy(record)

    for game in games:
        game_length = len(game)-1
        outcome = game[-1].values()[0]
        for state, i in zip(game, range(game_length)):
            if piece in state.values():
                for pos in state:
                    if state[pos] == piece:
                        helper[i][pos] += 1
                        output[i][pos+'P'] += 1 #inc existence score
                        if('w' in piece): #white piece
                            if(outcome == 'w'):
                                output[i][pos+'W'] += 1 #inc win score
                            elif(outcome == 'b'):
                                output[i][pos+'L'] += 1 #inc loss score
                            elif(outcome == 't'):
                                output[i][pos+'T'] += 1 #inc tie score
                        else: #black piece
                            if(outcome == 'b'):
                                output[i][pos+'W'] += 1 #inc win score
                            elif(outcome == 'w'):
                                output[i][pos+'L'] += 1 #inc loss score
                            elif(outcome == 't'):
                                output[i][pos+'T'] += 1 #inc tie score
                        break

    for game in games:
        game_length = len(game)-1
        outcome = game[-1].values()[0]
        for state, i in zip(game, range(game_length)):
            if piece in state.values():
                for pos in state:
                    if state[pos] == piece:
                        if(not output[i].has_key(pos+'W')):
                            output[i][pos+'W'] = 0
                        if(not output[i].has_key(pos+'L')):
                            output[i][pos+'L'] = 0
                        if(not output[i].has_key(pos+'T')):
                            output[i][pos+'T'] = 0

    for state in helper:
        total = sum(helper[state].values()) #total possible places of a piece at any given state
        output[state] = dict(output[state])
        score = 0
        print output[state]
        for pos in output[state]:
            if('P' in pos):
                output[state][pos] /= total
            elif('W' in pos):
                score += output[state][pos]
            elif('L' in pos):
                score += output[state][pos]
            elif('T' in pos):
                score += output[state][pos]
        for pos in output[state]:
            if('W' in pos):
                output[state][pos] /= score
            elif('L' in pos):
                output[state][pos] /= score
            elif('T' in pos):
                output[state][pos] /= score

    #delete empty records that may appear for some reason
    for k in list(output.keys()):
        if output[k] == {}:
            del output[k]

    return json.dumps(output)

if __name__ == '__main__':
    print 'Starting program...'
    games = readfile(sys.argv[1])
    pieces=['bR1','bR2','bN1','bN2','bB1','bB2','bQQ','bKK',
            'bP1','bP2','bP3','bP4','bP5','bP6','bP7','bP8',
            'wP1','wP2','wP3','wP4','wP5','wP6','wP7','wP8',
            'wR1','wR1','wN1','wN2','wB1','wB2','wQQ','wKK',
            ]
    print 'About to count pieces...'
    for piece in pieces:
      states = count(games,piece)
      print 'Writing piece %s to file...' % piece
      with open(piece+'.json', 'w') as log:
        print >>log, states
      print 'Successfully wrote %s to file!' % piece
    print 'Finished!'

