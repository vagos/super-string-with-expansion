import sys
import time
import itertools
import math
import random
from collections import defaultdict
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

    if n <= 0: raise Exception("Invalid input")

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
        if l in expansions:
            raise Exception("Invalid input")
        if len(set(rest)) != len(rest):
            raise Exception("Invalid input")
        expansions[l] = rest

    return string, expansions, strings

def is_expansion_valid(string, strings, expansion):
    def expand_string(string, expansion):
        for k in expansion:
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
            # print(f"Removing {k}", file=sys.stderr)
            del expansions[k]
    # If a possible expansion in the expansions is not a substring of string, remove it 
    for l in expansions:
        for s in set(expansions[l]):
            if s not in string:
                # print(f"Removing {s} from {l}", file=sys.stderr)
                expansions[l].remove(s)

# Handle the case where one of t_i strings is of the form AAA and there is no XXX in the target string
def can_handle_repeated_letters(string, expansions, strings):
    def get_repeated_letter_count(string):
        c = ''
        count = 0
        max_count = 0
        for i in range(len(string)):
            if string[i] == c:
                count += 1
                max_count = max(max_count, count)
            else:
                c = string[i]
                count = 1
        return max_count

    n_repeated_letters_string = get_repeated_letter_count(string)
    # print(f"n_repeated_letters_string = {n_repeated_letters_string}", file=sys.stderr)


    for s in strings:
        n_repeated_letters_s = get_repeated_letter_count(s)
        if n_repeated_letters_s == 0: continue
        # print(f"s = {s}, n_repeated_letters_s = {n_repeated_letters_s}", file=sys.stderr)
        if n_repeated_letters_s > n_repeated_letters_string:
            return False
    return True
        

def run_brute_force(string, expansions, strings):
    keys, values = zip(*expansions.items())
    for v in itertools.product(*values):
        expansion = dict(zip(keys, v))
        # print(f"Trying {expansion}", file=sys.stderr)
        
        if is_expansion_valid(string, strings, expansion):
            return expansion
    return None

def print_answer(expansion, expansions):
    for k in expansions.keys():
        if k not in expansion:
            expansion[k] = random.choice(list(expansions[k]))
    for k,v in expansion.items():
        print(f"{k}:{v}")

def print_no():
    print("NO")
    exit(0)

def main():
    random.seed(42)
    expansions = {}
    string = ""
    strings = set()
    expansions_cpy = {}

    try:
        string, expansions, strings = read_data()
        expansions_cpy = dict(expansions)
    except:
        print_no()

    if not can_handle_repeated_letters(string, expansions, strings):
        print_no()
    remove_invalid_choices(string, expansions, strings)
    if expansions:
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
