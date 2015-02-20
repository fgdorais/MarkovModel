from __future__ import print_function   # Python 2/3 compatibility #
from __future__ import unicode_literals # Python 2/3 compatibility #

import sys
import argparse

from trainer import MarkovTrainer

parser = argparse.ArgumentParser(description='Markov model trainer.')

parser.add_argument('text', help='training data', nargs='*',
                    type=argparse.FileType('r'), default=sys.stdin)
parser.add_argument('-d', '--depth', help='memory depth',
                    nargs=1, type=int, default=[3])
parser.add_argument('-m', '--model', help='output file for model',
                    nargs=1, default=['model.dat'])

args = parser.parse_args()

if args.depth[0] < 0:
    exit('{0}: error: argument -d/--depth: invalid negative value: {1}'.format(sys.argv[0], args.depth[0]))
    
Trainer = MarkovTrainer(args.depth[0])

for data in args.text:
    Trainer.train(data)

Trainer.save(args.model[0])

