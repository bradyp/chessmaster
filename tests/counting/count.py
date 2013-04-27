"""
Notes:
http://stackoverflow.com/questions/1894269/convert-string-list-to-list-in-python (parsing file)

"""
import string
import ast, sys, copy, json
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
    for entry in games:
        game = ast.literal_eval(entry)
        refined_game = []
        for state in game:
            refined_game.append(dict(zip(id,state)))
        output.append(refined_game)
    return output
    pass

def count(games, piece):
    """
    INPUT: list of games where a game is a list of states where a state is a list of moves where a move is a character of the form color/piece/numerical identifier, and piece identifier
    OUTPUT: list states, each state is a dict with id for key and a dict for the value, the dict will have keys of unique pieceid and values of how many occured there
    NEW_OUTPUT:dictionary of states with ints for keys and dicts for values, the values

    Ex: output: {0:{A1:0,A2:0.03,...G8:0.05}, 1:{...}, ...}
    """
    #prepare
    record = defaultdict(float) #this is an instance of the lowest most
    longest = max([len(game) for game in games])
    output = {}
    for i in range(longest):
        output[i] = copy.deepcopy(record)

    for game in games:
        for state, i in zip(game, range(len(game))):
            if piece in state.values():
                for pos in state:
                    if state[pos] == piece:
                        output[i][pos] += 1
                        break
    for state in output:
        total = sum(output[state].values()) #total possible places of a piece at any given state
        output[state] = dict(output[state])
        for pos in output[state]:
            output[state][pos] /= total
    return output
    pass

if __name__ == '__main__':
    games = readfile(sys.argv[1])
    states = count(games,string.lower('wP1'))
    print states
