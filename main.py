import sys
import time
import itertools
import math
import re
from collections import defaultdict

# Getting data from stdin
class Parser:
    def __init__(self):
        self.cursor = self.parse()
    def get_word(self):
        return next(self.cursor, None)
    def get_number(self):
        n = self.get_word()
        if n is None: return None
        return int(n)
    def parse(self):
        lines = sys.stdin.readlines()
        for line in lines:
            data = [s.strip() for s in line.split(' ')]
            for number in data:
                yield(number)   

def read_data():
    Sigma = "abcedfghijklmnopqrstuvwxyz"
    Gamma = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    parser = Parser()
    expansions = {}
    strings = set()
    k  = parser.get_number()
    string = parser.get_word()

    if k  < 0: raise Exception("Invalid input")

    for i in range(k):
        s = parser.get_word()
        # Invalid k  value.
        # We parsed some of the subsets before the strings were done.
        if ':' in s: raise Exception("Invalid input")
        strings.add(s)

    while True:
        s = parser.get_word()
        # Reached EOF
        if s is None: break 

        l, rest = s.split(':')
        # Invalid letter assigned to subset R_j
        if l not in Gamma or l == '': 
            raise Exception("Invalid input")

        R = rest.split(',')
        # r_j repeated
        if l in expansions: raise Exception("Invalid input")
        # R_j multiset
        if len(set(R)) != len(R):
            raise Exception("Invalid input")
        expansions[l] = R

    return string, expansions, strings

def remove_invalid_choices(string, expansions, strings):
    # Remove expansion of keys that do not appear into the target string (s)
    letters = set()
    for s in strings:
        letters = letters.union(set(s))
    for k in set(expansions.keys()):
        if k not in letters:
            del expansions[k]

    # If a possible expansion is not a substring of string (s), remove it 
    for l in expansions:
        for s in set(expansions[l]):
            if s not in string:
                expansions[l].remove(s)
    
    for e in expansions:
        if len(expansions[e]) == 0:
            del expansions[e]

    # If one of strings contains a letter to which no expansion is assigned, problem is unsolvable
    letters = set()
    for s in strings:
        letters = letters.union(set([c for c in s if c.isupper()]))

    for l in letters:
        if l not in expansions.keys():
            return False

    return True

def run_brute_force(string, expansions, strings):

    def is_expansion_valid(string, strings, expansion):
        translation = str.maketrans(expansion)

        for s in strings:
            s = s.translate(translation)
            if not s in string: # Is s substring of string?
                return False
        return True

    keys, values = zip(*expansions.items())
    for v in itertools.product(*values):
        # Iterate over all possible assignment of expansion to letters in Gamma
        expansion = dict(zip(keys, v))
        
        # If the assignement makes it so all string t_i are substrings of string s, we found a solution
        if is_expansion_valid(string, strings, expansion):
            return expansion
    return None

def print_answer(expansion, expansions):
    for k in expansions.keys():
        # If a letter in Gamma didn't appear in any of the t_i strings, assign it to the first possible expansion
        if k not in expansion:
            expansion[k] = expansions[k][0]
    for k,v in expansion.items():
        print(f"{k}:{v}")

def print_no():
    print("NO")
    exit(0)

def main():
    expansions = {} # Dictionary that maps letters in Gamma to subset R_j
    string = ""     # Target string s
    strings = set() # Set of strings t_i
    expansions_cpy = {}

    try:
        string, expansions, strings = read_data()
    except:
        print_no()

    expansions_cpy = {key: value[:] for key, value in expansions.items()}

    solvable = remove_invalid_choices(string, expansions, strings)

    if expansions and solvable:
        answer =  run_brute_force(string, expansions, strings)
    else:
        answer = None
    
    if expansions == {}:
        answer = {}

    if answer is not None:
        print_answer(answer, expansions_cpy)
    else:
        print_no()

if __name__ == '__main__':
    main()
