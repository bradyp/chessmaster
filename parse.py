from collections import defaultdict
from itertools import izip

import re
import sys


def _parse_moves(token):
    '''                                                                                            
    Parse a moves token and returns a list with moviments                                          
    '''
    moves = []
    while token:
        token = re.sub(r'^\s*(\d+\.+\s*)?', '', token)

        if token.startswith('{'):
            pos = token.find('}')+1
        else:
            pos1 = token.find(' ')
            pos2 = token.find('{')
            if pos1 <= 0:
                pos = pos2
            elif pos2 <= 0:
                pos = pos1
            else:
                pos = min([pos1, pos2])

        if pos > 0:
            moves.append(token[:pos])
            token = token[pos:]
        else:
            moves.append(token)
            token = ''

    return moves


def parse_entry(entry):
    output = {'history':''}
    for elem in entry.split('\n'):
        elem = elem.replace('[','')
        elem = elem.replace(']','')
        elem = elem.split('\"')
        if '' in elem:
            elem.remove('')
        if len(elem) == 2:
            output[elem[0]] = elem[1]
        elif len(elem) == 1:
            output['history'] += elem[0]
    output['history'] = parse_history(output['history'])
    return output
pass

def parse_history(hist):
    first = re.split('(\d+\.)',hist)
    del first[0]
    second = []
    for item in first:
        second.append(item.replace('.',''))
    i = iter(second)
    output = dict(izip(i, i))
    return output
pass

def parse(filename):
    f = open(filename, 'r')
    body = f.read().replace('\n','')
    body = body.replace('\r','')
    body = re.sub(r'\[.*?\]', '@', body)
    body = body.split('@')

    while '' in body:
        body.remove('')
    return body
pass

if __name__ == '__main__':
    games = parse(sys.argv[1])
    print games[0]
    print _parse_moves(games[0])
#    print parse_history(games[0])
    #data = [parse_history(entry) for entry in games]
    #for entry in data:
    #    print 'New Game'
    #    for move in entry:
    #        print move, entry[move]
    #    print '----------'
pass
