
import json
import re
import sys

def readfile(filename):
    f = open(filename)
    games = f.read().split('@')
    print f.read()
    f.close()
    return games
    pass

if __name__ == '__main__':
    games = readfile(sys.argv[1])
    print len(games)
    print json.loads(games[0])
