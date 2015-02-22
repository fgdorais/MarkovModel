import sys
import csv

# Module csv in Python 2 doesn't natively support unicode, so utf-8
# encoding/decoding must be done manually. Python 2 csv also requires
# for files to be opened in binary mode.
if sys.version_info[0] == 3:
    def encode(s):
        return s
    def decode(s):
        return s
    def csvopen(file, mode):
        return open(file, mode, newline='', encoding='utf-8')
elif sys.version_info[0] == 2:
    def encode(s):
        return s.encode('utf-8')
    def decode(s):
        return unicode(s, 'utf-8')
    def csvopen(file, mode):
        return open(file, mode + 'b')

# Markov dialect for csv

# By default, tabs are used as delimiters since other characters are
# likely to occur in tokens from natural languages.

csv.register_dialect('markov',
                     delimiter='\t',
                     doublequote=True,
                     quoting=csv.QUOTE_NONNUMERIC,
                     skipinitialspace=True,
                     strict=False)

# Sparse model I/O

def read_sparse(filename, sorted=False):
    """Read sparse model from file"""
    
    model = {}
    with csvopen(filename, 'r') as datafile:
        datareader = csv.reader(datafile, dialect='markov')
        for row in datareader:
            model[decode(row[0])] = [(decode(row[i]),row[i+1]) for i in range(1,len(row),2)]
        if sorted:
            model[decode(row[0])].sort(key=lambda x: x[1], reverse=True)
    return model

def write_sparse(filename, model):
    """Write sparse model to file"""
    
    with csvopen(filename, 'w') as datafile:
        datawriter = csv.writer(datafile, dialect='markov')
        for ctx in model:
            row = [encode(ctx)]
            for tok, prb in model[ctx]:
                row += [encode(tok), prb]
            datawriter.writerow(row)

# Matrix model I/O

def read_matrix(filename, tokens=None, sorted=False):
    """Read transition matrix from file"""
    
    with csvopen(filename, 'r') as datafile:
        if tokens:
            datareader = csv.DictReader(datafile, dialect='markov',
                                        fieldnames=[encode(x) for x in tokens])
        else:
            datareader = csv.DictReader(datafile, dialect='markov')
            tokens = [decode(x) for x in datareader.fieldnames]

        # set empty context with uniform distribution
        model = {u'' : [(tok,1.0/len(tokens)) for tok in tokens]}

        # read single token contexts from transition matrix
        for ctx in tokens:
            row = next(datareader)
            # omit zero entries
            model[ctx] = [(decode(tok),row[tok]) for tok in row if row[tok] > 0.0]
            if sorted:
                model[ctx].sort(key=lambda x: x[1], reverse=True)
        return model

def write_matrix(filename, model, tokens=None):
    """Write transition matrix to file"""
    
    with csvopen(filename, 'w') as datafile:
        if not tokens:
            tokens = [encode(tok) for tok, prb in model[u'']]
            header = False
        else:
            header = True
        datawriter = csv.DictWriter(datafile, tokens, restval=0.0, dialect='markov')
        if header:
            datawriter.writeheader()
        for ctx in tokens:
            # default to empty context if ctx is not present in model
            row = model.get(decode(ctx), model[u''])
            datawriter.writerow(dict((encode(tok),prb) for tok, prb in row))

