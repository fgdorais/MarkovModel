from __future__ import print_function   # Python 2/3 compatibility #
from __future__ import unicode_literals # Python 2/3 compatibility #
from functools import reduce            # Python 2/3 compatibility #

import sys
import argparse

from trainer import MarkovTrainer
from generator import MarkovGenerator

parser = argparse.ArgumentParser(description='Markov model trainer.')
subparsers = parser.add_subparsers(help='sub-command help')

# 'train' command parser
train_parser = subparsers.add_parser('train', help='train model using text data')
train_parser.add_argument('model', help='output model', nargs=1)
train_parser.add_argument('text', help='training data', nargs='*',
                          type=argparse.FileType('r'), default=sys.stdin)
train_parser.add_argument('-d', '--depth', help='memory depth',
                          nargs=1, type=int, default=[3])

def train(args):
    """Command for training a new Markov model."""
    
    if args.depth[0] < 0:
        exit('{0}: error: argument -d/--depth: invalid negative value: {1}'.format(sys.argv[0], args.depth[0]))
    
    Trainer = MarkovTrainer(args.depth[0])

    for data in args.text:
        Trainer.train(data)

    Trainer.save(args.model[0])

train_parser.set_defaults(func=train)

# 'random' command parser
random_parser = subparsers.add_parser('random', help='generate random text using model')
random_parser.add_argument('model', help='input model', nargs=1)
random_parser.add_argument('count', help='token count', nargs='?', type=int, default=100)
random_parser.add_argument('-d', '--depth', help='memory depth',
                           nargs=1, type=int, default=[3])

def random(args):
    """Command for generating random data using a Markov model."""

    if args.depth[0] < 0:
        exit('{0}: error: argument -d/--depth: invalid negative value: {1}'.format(sys.argv[0], args.depth[0]))

    Generator = MarkovGenerator(args.model[0], depth=args.depth[0])

    if args.count > 0:
        print(reduce(lambda x, y: x + ' ' + y, [Generator.next() for i in range(args.count)]))

random_parser.set_defaults(func=random)

args = parser.parse_args()
args.func(args)
