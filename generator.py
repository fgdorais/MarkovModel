from __future__ import unicode_literals # Python 2/3 compatibility #
from codecs import open                 # Python 2/3 compatibility #
from functools import reduce            # Python 2/3 compatibility #
import random

def dequote(s, validate=True):
    if validate:
        if not (s[0] == '"' and s[-1] == '"'):
            raise ValueError
        r = ''
        q = False
        for c in s[1:-1]:
            if q:
                if c != '"':
                    raise ValueError
                q = False
            else:
                r += c
                q = (c == '"')
        if q:
            raise ValueError
        return r
    else:
        return s[1:-1].replace('""','"')

class MarkovGenerator:
    """Generate random text using Markov model"""

    def __init__(self, filename, depth=3):
        self.depth = depth
        self.thist = []
        self.model = {}
        
        with open(filename, 'r', encoding='utf-8') as datafile:
            for line in datafile:
                data = line.split('\t')

                ctx = dequote(data[0])
                self.model[ctx] = []

                for i in range(1,len(data),2):
                    self.model[ctx].append((dequote(data[i]), float(data[i+1])))
                    
    def __iter__(self):
        return self

    def __next__(self):
        self.next()

    def next(self):
        """Get next random token"""

        # find longest context within model      
        for i in range(len(self.thist)):
            ctx = reduce(lambda x, y: x + ' ' + y, self.thist[i:])
            if ctx in self.model:
                return self.generate(ctx)
        # default to empty context
        return self.generate('')

    def generate(self, ctx):
        """Generate a random token from given context"""
        
        prob = random.random()
        for j in range(len(self.model[ctx])):
            if prob <= self.model[ctx][j][1]:
                tok = self.model[ctx][j][0]
                self.thist.append(tok)
                if len(self.thist) > self.depth:
                    del self.thist[0]
                return tok
            else:
                prob -= self.model[ctx][j][1]

        # default to most probable token in case of roundoff errors 
        return self.model[0][0]
