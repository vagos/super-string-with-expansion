import sys
import itertools
import math
import random
# Getting data from stdin
class Parser:
    def __init__(self, file=None):
        self.cursor = self.parse()
        self.file = file
    def get_word(self):
        return next(self.cursor, None)
    def get_number(self):
        n = self.get_word()
        if n is None: return None
        return int(n)
    def parse(self):
        if self.file:
            with open(self.file) as file:
                lines = file.readlines()
                for line in lines:
                    data = list(line.split(' '))
                    for number in data:
                        if len(number) > 0:
                            yield(number)   
        else:
            for line in sys.stdin:
                data = [s.strip() for s in line.split(' ')]
                for number in data:
                    yield(number)   

def read_data():
    file = None
    if len(sys.argv) > 1:
        file = sys.argv[1]
    parser = Parser(file)
    expansions = {}
    strings = set()
    n = parser.get_number()
    string = parser.get_word()
    for i in range(n):
        s = parser.get_word()
        # Invalid n value.
        # We parsed some of the subsets before the strings were done.
        if ':' in s: raise Exception("Invalid input")
        strings.add(s)
    while True:
        s = parser.get_word()
        if s is None: break # Reached EOF

        l, rest = s.split(':')
        rest = rest.split(',')
        expansions[l] = rest
    return string, expansions, strings

def is_expansion_valid(string, strings, expansion):
    def expand_string(string, expansion):
        for k in expansion:
            if k not in string: pass
            string = string.replace(k, expansion[k])
        return string
    for s in strings:
        s = expand_string(s, expansion)
        if not s in string: # Is s substring of string?
            return False
    return True

def remove_invalid_choices(string, expansions, strings):
    # Remove expansion of keys that do not appear into the target
    letters = set()
    for s in strings:
        letters = letters.union(set(s))
    for k in set(expansions.keys()):
        if k not in letters:
            del expansions[k]
    # If a possible expansion in the expansions is not a substring of string, remove it 
    for l in expansions:
        for s in set(expansions[l]):
            if s not in string:
                expansions[l].remove(s)

def run_brute_force(string, expansions, strings):
    keys, values = zip(*expansions.items())
    for v in itertools.product(*values):
        expansion = dict(zip(keys, v))
        
        if is_expansion_valid(string, strings, expansion):
            return expansion
    return None

def print_answer(expansion, expansions):
    for k in expansions.keys():
        if k not in expansion:
            expansion[k] = random.choice(expansions[k])
    for k,v in expansion.items():
        print(f"{k}:{v}")

def main():
    random.seed(42)
    try:
        string, expansions, strings = read_data()
        expansions_cpy = dict(expansions)
    except:
        answer = None
    try:
        remove_invalid_choices(string, expansions, strings)
        answer =  run_brute_force(string, expansions, strings)
    except:
        answer = None
    if answer:
        print_answer(answer, expansions_cpy)
    else:
        print("NO")

if __name__ == '__main__':
    main()
