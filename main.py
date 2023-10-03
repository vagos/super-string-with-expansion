import sys
import itertools
import math

# Getting data from stdin

class Parser:

    def __init__(self, file=None):
        self.cursor = self.parse()
        self.file = file

    def get_word(self):
        return next(self.cursor)

    def get_number(self):
        return int(self.get_word())

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
            while True:
                data = list(input().split(' '))
                for number in data:
                    if len(number) > 0:
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
        strings.add(s)

    while True:
        try:
            s = parser.get_word()
            l, rest = s.split(':')
            expansions[l] = rest.split(',')
        except:
            break

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


def run_brute_force(string, expansions, strings):
    keys, values = zip(*expansions.items())

    for v in itertools.product(*values):
        expansion = dict(zip(keys, v))
        
        if is_expansion_valid(string, strings, expansion):
            return expansion

    return None

def print_answer(expansion):
    for k,v in expansion.items():
        print(f"{k}:{v}")

def main():
    string, expansions, strings = read_data()
    answer =  run_brute_force(string, expansions, strings)

    if answer:
        print_answer(answer)
    else:
        print("NO")

if __name__ == '__main__':
    main()
