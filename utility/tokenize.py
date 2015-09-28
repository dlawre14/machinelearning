#tokenize a string
import re

def tokenize(string, **kwargs):
    #ignore kwargs for now
    string = re.sub('[.,!?:;]', '', string)
    return string.lower().split()
