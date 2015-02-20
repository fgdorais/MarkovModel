from __future__ import print_function   # Python 2/3 compatibility #
from __future__ import unicode_literals # Python 2/3 compatibility #
from functools import reduce            # Python 2/3 compatibility #

import sys
import argparse

from generator import *

parser = argparse.ArgumentParser(description='Markov model random text generator.')

parser.add_argument('count', help='token count',
                    nargs='?', type=int, default=100)
parser.add_argument('-d', '--depth', help='memory depth',
                    nargs=1, type=int, default=[3])
parser.add_argument('-m', '--model', help='model data',
                    nargs=1, default=['model.dat'])

args = parser.parse_args()

if args.depth[0] < 0:
    exit('{0}: error: argument -d/--depth: invalid negative value: {1}'.format(sys.argv[0], args.depth[0]))

Generator = MarkovGenerator(args.model[0], depth=args.depth[0])

if args.count > 0:
    print(reduce(lambda x, y: x + ' ' + y,
                 [Generator.next() for i in range(args.count)]))


