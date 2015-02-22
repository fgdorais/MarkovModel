from __future__ import unicode_literals # Python 2/3 compatibility #
from __future__ import print_function   # Python 2/3 compatibility #

import sys
import argparse

import modelio
from parser import TokenParser
from trainer import MarkovTrainer
from generator import MarkovGenerator

parser = argparse.ArgumentParser(description='Markov model trainer.')
subparsers = parser.add_subparsers(help='sub-command help')

# 'train' command parser
train_parser = subparsers.add_parser('train', help='train model using text data')
train_parser.add_argument('model', help='output model', nargs=1)
train_parser.add_argument('text', help='training data', nargs='*', type=argparse.FileType('r'), default=sys.stdin)
train_parser.add_argument('-d', '--depth', help='memory depth', nargs=1, type=int, default=[1])
train_parser.add_argument('--matrix', help='matrix format', action="store_true")

def train(args):
    """Command for training a new Markov model."""
    
    if args.depth[0] < 0:
        exit('{0}: error: argument -d/--depth: invalid negative value: {1}'.format(sys.argv[0], args.depth[0]))
    
    Trainer = MarkovTrainer(args.depth[0])
    
    for data in args.text:
        Trainer.train(TokenParser(data))
    
    if args.matrix:
        modelio.write_matrix(args.model[0], Trainer.model())
    else:
        modelio.write_sparse(args.model[0], Trainer.model())

train_parser.set_defaults(func=train)

# 'random' command parser
random_parser = subparsers.add_parser('random', help='generate random text using model')
random_parser.add_argument('model', help='input model', nargs=1)
random_parser.add_argument('count', help='token count', nargs='?', type=int, default=100)
random_parser.add_argument('-d', '--depth', help='memory depth', nargs=1, type=int, default=[1])
random_parser.add_argument('--matrix', help='matrix format', action="store_true")

def random(args):
    """Command for generating random data using a Markov model."""
    
    if args.depth[0] < 0:
        exit('{0}: error: argument -d/--depth: invalid negative value: {1}'.format(sys.argv[0], args.depth[0]))
    if args.count <= 0:
        exit('{0}: error: token count must be positive, got: {1}.'.format(sys.argv[0], args.count))
    
    if args.matrix:
        model = modelio.read_matrix(args.model[0])
        args.depth[0] = 1 # Force depth 1 for matrix format
    else:
        model = modelio.read_sparse(args.model[0])
    
    Generator = MarkovGenerator(model, depth=args.depth[0])
    
    print(' '.join([Generator.next() for i in range(args.count)]))

random_parser.set_defaults(func=random)

args = parser.parse_args()
args.func(args)
