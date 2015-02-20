from __future__ import unicode_literals # Python 2/3 compatibility #
from codecs import open, getreader      # Python 2/3 compatibility #
import unicodedata

class TokenParser:
    """Parse a Unicode text stream into space/control separated tokens

    Space and control characters are identified using Unicode general
    category values as defined in section 4.5 of The Unicode Standard,
    Version 7.0.0.
    """

    def __init__(self, stream):
        self.stream = getreader('utf-8')(stream) # Python 2/3 compatibility #
        self.tokens = []

    def __iter__(self):
        return self

    def __next__(self):
        self.next() # Python 2/3 compatibility #
    
    def next(self):
        """Get next token"""

        while not self.tokens:
            try:
                self.fill()
            except:
                raise StopIteration            

        return self.tokens.pop(0)

    def fill(self):
        """Fill the token queue from stream"""

        line = self.stream.readline()

        if not line:
            raise EOFError
        
        word = ''
        for c in line:
            if unicodedata.category(c)[0] in 'LMNSP':
                # Letter, Mark, Number, Symbol, Punctuation
                word += c
            elif unicodedata.category(c)[0] in 'ZC':
                # Spacing, Control
                if word:
                    self.tokens.append(word)
                word = ''
        if word:
            # only reached if file does not end with a newline
            self.tokens.append(word)
