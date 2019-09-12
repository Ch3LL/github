import argparse

parser = argparse.ArgumentParser()

# pr.py arguments
parser.add_argument('--commit',
                    help='Query PR for individual commit')

parser.add_argument('--range',
                    help='Query PRs between a range',
                    action='store_true')
parser.add_argument('-c1', '--commit1',
                    help='First commit in range')
parser.add_argument('-c2', '--commit2',
                    help='Second commit in range')

args = parser.parse_args()
