from lib2to3.pgen2 import grammar
from nltk.parse.generate import generate
from nltk import CFG
import random

d_grammar = """
S -> Ad N
Ad -> 'beautiful' | 'must have' | 'clear' | 'elegant' | 'basic' | 'advanced'
N -> 'book' | 'paper' | 'printer' | 'monitor' | 'mouse' | 'pen' | 'pencil'
"""

p_grammar = """
S -> 'it' V Adv
V -> 'works' | 'plays' | 'prints' | 'displays' | 'sends'
Adv -> 'precise' | 'well' | 'quick' | 'nicely'
"""

g_grammar = """
S -> Adj 'for' V
Adj -> 'great' | 'best' | 'suitable' | 'excellent'
V -> 'printing' | 'displaying' | 'typing' | 'reading' | 'working'
"""

c_grammar = """
S -> C | I
C -> 'it comes with' A
I -> 'it includes' A
A -> 'cable' | 'power supply' | 'mouse' | 'connection' | 'extension' | 'adapter'
"""

q_grammar = """
S -> P | 
P -> 'Package contains ' Q | 'Box contains ' Q
Q -> '1' | '5' | '10' | '50' | '500'
"""


class Sentence:
    def __init__(self):
        grammar = CFG.fromstring(d_grammar)
        self.descriptions = list(generate(grammar, n=100))

        grammar = CFG.fromstring(p_grammar)
        self.phrases = list(generate(grammar, n=100))

        grammar = CFG.fromstring(g_grammar)
        self.qualities = list(generate(grammar, n=100))

        grammar = CFG.fromstring(c_grammar)
        self.accessories = list(generate(grammar, n=100))

        grammar = CFG.fromstring(q_grammar)
        self.quantities = list(generate(grammar, n=100))

    def random_sentence(self):
        desc = self.descriptions[random.randrange(0, len(self.descriptions))]
        phrase = self.phrases[random.randrange(0, len(self.phrases))]
        quality = self.qualities[random.randrange(0, len(self.qualities))]
        accessory = self.accessories[random.randrange(0, len(self.accessories))]
        quantity = self.quantities[random.randrange(0, len(self.quantities))]

        return ' '.join(desc) + '. ' + ' '.join(phrase) + '. ' + ' '.join(quality) + '. ' + ' '.join(accessory) + '. ' + ' '.join(quantity) + '.' 


