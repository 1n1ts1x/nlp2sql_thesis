import nltk
from nltk import load_parser

class TextAnalysis:
    def __init__(self, q=''):
        self.q = q

    '''generate sql query via parsing'''
    def parse_tokens(self):
        #pos tagging
        pos_query = nltk.pos_tag(self.q)

        #parsing
        cp = load_parser('./test_sql.fcfg')
        trees = list(cp.parse(self.q))
        list_query = [x for x in trees[0].label()['SEM'] if x]

        print(' '.join(list_query))