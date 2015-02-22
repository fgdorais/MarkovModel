from __future__ import unicode_literals # Python 2/3 compatibility #

import random

class MarkovGenerator:
    """Generate random text using Markov model"""
    
    def __init__(self, model, depth=3):
        self.depth = depth
        self.model = model
        self.thist = []
        self.urand = random.random
    
    def __iter__(self):
        return self
    
    def __next__(self):
        self.next()
    
    def next(self):
        """Get next random token"""
        
        # find longest context within model
        for i in range(len(self.thist)):
            ctx = ' '.join(self.thist[i:])
            if ctx in self.model:
                return self.generate(ctx)
        
        # default to empty context
        return self.generate('')
    
    def seed(self, tokens):
        self.thist = tokens[-self.depth:]
    
    def generate(self, ctx):
        """Generate a random token from given context"""
        
        prob = self.urand()
        for j in range(len(self.model[ctx])):
            if prob <= self.model[ctx][j][1]:
                tok = self.model[ctx][j][0]
                self.thist.append(tok)
                if len(self.thist) > self.depth:
                    del self.thist[0]
                return tok
            else:
                prob -= self.model[ctx][j][1]
        
        # default in case of accumulated roundoff errors
        return self.model[ctx][0][0]

