from __future__ import print_function   # Python 2/3 compatibility #
from __future__ import unicode_literals # Python 2/3 compatibility #
from functools import reduce            # Python 2/3 compatibility #

from parser import *

def enquote(s, tabrepl=None):
    """Quote an input string, doubling any preexisting quotes"""

    if tabrepl:
        s = s.replace('\t', tabrepl)
    return '"' + s.replace('"','""') + '"'

class MarkovTrainer:

    def __init__(self, depth=3):
        self.model = {'': {}}
        self.depth = depth
        self.thist = []

    def clear_memory(self):
        """Clear the list of remembered tokens"""
        self.thist = []
        
    def train(self, stream):
        """Train Markov model using text data from stream"""

        for tok in TokenParser(stream):

            # First, deal with the empty context
            self.model[''][tok] = self.model[''].get(tok, 0) + 1

            # Then, deal with contexts from memory store
            for d in range(len(self.thist)):
                # Contexts are recorded a space-separated lists
                ctx = reduce(lambda x, y: x + ' ' + y, self.thist[d:])                
                if not ctx in self.model:
                    self.model[ctx] = {}
                self.model[ctx][tok] = self.model[ctx].get(tok, 0) + 1

            # Update memory store with new token
            self.thist.append(tok)
            if len(self.thist) > self.depth:
                del self.thist[0]

    def save(self, filename):
        """Save model to file <filename> (UTF-8 encoding)"""
        
        with open(filename, 'w', encoding='utf-8') as datafile:
            for ctx in self.model:
                total = sum(self.model[ctx].values())
                pdata = [(enquote(t[0]),1.0*t[1]/total)
                         for t in sorted(self.model[ctx].items(),
                                         key = lambda x: x[1],
                                         reverse = True)]  
                sline = reduce(lambda x, y: x + '\t' + y,
                               [enquote(ctx)] + ['{0[0]}\t{0[1]:.4e}'.format(t) for t in pdata])
                print(sline, file = datafile)
        

