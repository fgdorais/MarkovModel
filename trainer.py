from __future__ import unicode_literals # Python 2/3 compatibility #

from parser import TokenParser

class MarkovTrainer:

    def __init__(self, depth=3):
        self.tdata = {'': {}}
        self.depth = depth
        self.thist = []

    def clear_memory(self):
        """Clear the list of remembered tokens"""
        self.thist = []
        
    def train(self, stream):
        """Train Markov model using text data from stream"""

        for tok in TokenParser(stream):

            # First, deal with the empty context
            self.tdata[''][tok] = self.tdata[''].get(tok, 0) + 1

            # Then, deal with contexts from memory store
            for d in range(len(self.thist)):
                # Contexts are recorded a space-separated lists
                ctx = ' '.join(self.thist[d:])
                if not ctx in self.tdata:
                    self.tdata[ctx] = {}
                self.tdata[ctx][tok] = self.tdata[ctx].get(tok, 0) + 1

            # Update memory store with new token
            self.thist.append(tok)
            if len(self.thist) > self.depth:
                del self.thist[0]

    def model(self):
        """Get learned model"""

        model = {}
        for ctx in self.tdata:
            total = sum(self.tdata[ctx].values())
            model[ctx] = []
            for tok in self.tdata[ctx]:
                model[ctx].append((tok, float(self.tdata[ctx][tok])/total))
        return model
