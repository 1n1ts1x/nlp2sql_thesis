import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

class CleanText:
    def __init__(self, q='', save_for_later=[], pff=True):
        self.q = q
        self.tokens2 = ''
        self.stopwords2 = ''
        self.lemmatized_tokens2 = ''
        self.params = ['temperature', 'humidity', 'soil', 'light', 'air', 'all', 'date']
        self.save_for_later = save_for_later
        self.pff = pff

    def arrange_tokens(self, ls, cmd_list):
        month_list = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
        cmd = None
        month = None

        try: 
            i = 0

            while i < len(ls):
                if ls[i] == 'the' and ls[i + 1] == 'date' and ls[i + 2] == 'is':
                    ls[i] = ''
                    ls[i + 1] = ''
                    ls [i + 2] = ''
                elif ls[i] == 'date' and ls[i + 1] == 'is':
                    ls[i] = ''
                    ls[i + 1] = ''
                    
                i += 1
        except:
            pass
            
        ls = [x for x in ls if x != '']

        cmd = None
        month = None

        i = 0

        while i < len(ls):
            j = 0
            
            while j < len(month_list):
                if month_list[j] == ls[i]:
                    month = month_list[j]
                    break
                j += 1
            
            if month:
                break
            
            i += 1

        i = 0

        while i < len(ls):
            j = 0
            
            while j < len(cmd_list):
                if cmd_list[j] == ls[i]:
                    cmd = cmd_list[j]
                    break
                j += 1
            
            if cmd:
                break
            
            i += 1
            
        index = index2 = index3 = index4 = index5 = index6 = index7 = index8 = index9 = index10 = 0

        try:
            if 'today' in ls and month:
                list_date = []
            
                i = len(ls) - 1
            
                while i >= 0:
                    j = i
                
                    if ls[i] == 'today':
                        index5 = i
                        while j >= 0:
                            if ls[j] != 'table' and ls[j] != 'degree' and ls[j] != 'percent' and ls[j] != 'lux' and ls[j] != 'ppm' and ls[j] != 'temperature' and ls[j] != 'soil' and ls[j] != 'humidity' and ls[j] != 'air' and ls[j] != 'light' and not ls[j].isnumeric() and ls[j] != 'table' and ls[j] != 'readings' and ls[j] != 'reading' and ls[j] != month:
                                list_date.append(ls[j])
                            else:
                                break
                            
                            index6 = j
                            j -= 1
                    i -= 1    
            
                list_date.reverse()
            
                i = 0
                
                list_cmd = []
                list_table = []
                list_condition = []
                list_date2 = []
                ffdate = 0
                ffdate2 = 0
                ffdate3 = 0
                
                while i < len(ls):
                    j = i
                    
                    if ls[i] == cmd:
                        index = i
                        while j < len(ls):
                            if ls[j] != 'of' and ls[j] != 'where' and ls[j] != 'on' and ls[j] != ls[index5] and ls[j] != ls[index6] and ls[j] != 'today' and ls[j] != 'above' and ls[j] != 'below' and ls[j] != 'not' and 'today' in ls:
                                list_cmd.append(ls[j])
            
                            else:
                                break
                            
                            index2 = j
                            j += 1
            
                    elif ls[i] == 'of' and (ls[i + 2] == 'table' or ls[i + 3] == 'table'):
                        index3 = i
                        while j < len(ls):
                            if ls[j] != ls[index5] and ls[j] != 'where' and ls[j] != cmd and ls[j] != 'is' and ls[j] != 'not' and ls[j] != 'above' and ls[j] != 'below' and ls[j] != 'equal' and ls[j] != ls[index6] and ls[j] != 'on' and ls[j] != 'and' and ls[j] != 'or' and ls[j] != 'on' and 'today' in ls and ls[j] != 'today' and 'today' in ls:
                                list_table.append(ls[j])
            
                            else:
                                break
                            
                            index4 = j
                            j += 1
                            
                    elif ls[i] == 'and' and ls[i + 1] == 'is' and ls[i+2] == 'not' and (ls[i + 3] == 'on' or ls[i + 3] == 'above' or ls[i + 3] == 'below') and (ls[i + 4] == month or ls[i + 5] == month or ls[i + 6] == month):
                        index9 = i
                        while j < len(ls):
                            if ls[j] != 'table' and ls[j] != 'degree' and ls[j] != 'percent' and ls[j] != 'lux' and ls[j] != 'ppm' and ls[j] != 'temperature' and ls[j] != 'soil' and ls[j] != 'humidity' and ls[j] != 'air' and ls[j] != 'light'and ls[j] != 'table' and ls[j] != 'where' and ls[j] != cmd and ls[j] != 'today' and ls[j] != 'of':
                                list_date2.append(ls[j])
                                ffdate3 = 1
                                ffdate2 = 1
                                ffdate = 1
                            else:
                                break
                            
                            index10 = j
                            j += 1
                            
                    elif not ffdate3 and ls[i] == 'and' and (ls[i + 1] == 'not' or ls[i + 1] == 'is') and (ls[i + 2] == 'on' or ls[i + 2] == 'above' or ls[i + 2] == 'below') and (ls[i + 3] == month or ls[i + 4] == month or ls[i + 5] == month):
                        index9 = i
                        while j < len(ls):
                            if ls[j] != 'table' and ls[j] != 'degree' and ls[j] != 'percent' and ls[j] != 'lux' and ls[j] != 'ppm' and ls[j] != 'temperature' and ls[j] != 'soil' and ls[j] != 'humidity' and ls[j] != 'air' and ls[j] != 'light'and ls[j] != 'table' and ls[j] != 'where' and ls[j] != cmd and ls[j] != 'today' and ls[j] != 'of':
                                list_date2.append(ls[j])
                                
                                ffdate2 = 1
                                ffdate = 1
                            else:
                                break
                            
                            index10 = j
                            j += 1
                    elif not ffdate2 and ls[i] == 'not' and (ls[i + 1] == 'on' or ls[i + 1] == 'above' or ls[i + 1] == 'below') and (ls[i + 2] == month or ls[i + 3] == month or ls[i + 4] == month):
                        index9 = i
                        while j < len(ls):
                            if ls[j] != 'table' and ls[j] != 'degree' and ls[j] != 'percent' and ls[j] != 'lux' and ls[j] != 'ppm' and ls[j] != 'temperature' and ls[j] != 'soil' and ls[j] != 'humidity' and ls[j] != 'air' and ls[j] != 'light'and ls[j] != 'table' and ls[j] != 'where' and ls[j] != cmd and ls[j] != 'today' and ls[j] != 'of':
                                list_date2.append(ls[j])
                                ffdate = 1
                            else:
                                break
                            
                            index10 = j
                            j += 1
                            
                    elif not ffdate and (ls[i] == 'on' or ls[i] == 'above' or ls[i] == 'below' or  ls[i] == 'and' or ls[i] == 'or') and (ls[i + 1] == month or ls[i + 2] == month or ls[i + 3] == month):
                        index7 = i
                        while j < len(ls):
                            if ls[j] != 'table' and ls[j] != 'degree' and ls[j] != 'percent' and ls[j] != 'lux' and ls[j] != 'ppm' and ls[j] != 'temperature' and ls[j] != 'soil' and ls[j] != 'humidity' and ls[j] != 'air' and ls[j] != 'light'and ls[j] != 'table' and ls[j] != 'where' and ls[j] != cmd and ls[j] != 'today' and ls[j] != 'of':
                                list_date2.append(ls[j])
                            else:
                                break
                            
                            index8 = j
                            j += 1
                            
                    i += 1
            
            elif 'today' in ls:
                list_date = []
            
                i = len(ls) - 1
            
                while i >= 0:
                    j = i
                
                    if ls[i] == 'today':
                        index5 = i
                        while j >= 0:
                            if ls[j] != 'table' and ls[j] != 'degree' and ls[j] != 'percent' and ls[j] != 'lux' and ls[j] != 'ppm' and ls[j] != 'temperature' and ls[j] != 'soil' and ls[j] != 'humidity' and ls[j] != 'air' and ls[j] != 'light' and not ls[j].isnumeric() and ls[j] != 'table' and ls[j] != 'readings' and ls[j] != 'reading' and ls[j] != month:
                                list_date.append(ls[j])
                            else:
                                break
                            
                            index6 = j
                            j -= 1
                    i -= 1    
            
                list_date.reverse()
            
                i = 0
                
                list_cmd = []
                list_table = []
                list_condition = []
                list_date2 = []
                ffdate = 0
                ffdate2 = 0
                ffdate3 = 0
                
                while i < len(ls):
                    j = i
                    
                    if ls[i] == cmd:
                        index = i
                        while j < len(ls):
                            if ls[j] != 'of' and ls[j] != 'where' and ls[j] != 'on' and ls[j] != ls[index5] and ls[j] != ls[index6] and ls[j] != 'today' and ls[j] != 'above' and ls[j] != 'below' and ls[j] != 'not' and 'today' in ls:
                                list_cmd.append(ls[j])
            
                            else:
                                break
                            
                            index2 = j
                            j += 1
            
                    elif ls[i] == 'of' and (ls[i + 2] == 'table' or ls[i + 3] == 'table'):
                        index3 = i
                        while j < len(ls):
                            if ls[j] != ls[index5] and ls[j] != 'where' and ls[j] != cmd and ls[j] != 'is' and ls[j] != 'not' and ls[j] != 'above' and ls[j] != 'below' and ls[j] != 'equal' and ls[j] != ls[index6] and ls[j] != 'on' and ls[j] != 'and' and ls[j] != 'or' and ls[j] != 'on' and 'today' in ls and ls[j] != 'today' and 'today' in ls:
                                list_table.append(ls[j])
            
                            else:
                                break
                            
                            index4 = j
                            j += 1
                            
                    i += 1
            
            elif month:
                    i = 0
                    
                    list_cmd = []
                    list_table = []
                    list_condition = []
                    list_date2 = []
                    ffdate = 0
                    ffdate2 = 0
                    ffdate3 = 0
                    
                    while i < len(ls):
                        j = i
                        
                        if ls[i] == cmd:
                            index = i
                            while j < len(ls):
                                if ls[j] != 'of' and ls[j] != 'where' and ls[j] != 'on' and ls[j] != 'above' and ls[j] != 'below' and ls[j] != 'not':
                                    list_cmd.append(ls[j])
                
                                else:
                                    break
                                
                                index2 = j
                                j += 1
                
                        elif ls[i] == 'of' and (ls[i + 2] == 'table' or ls[i + 3] == 'table'):
                            index3 = i
                            while j < len(ls):
                                if ls[j] != 'where' and ls[j] != cmd and ls[j] != 'is' and ls[j] != 'not' and ls[j] != 'above' and ls[j] != 'below' and ls[j] != 'equal' and ls[j] != 'on' and ls[j] != 'and' and ls[j] != 'or' and ls[j] != 'on':
                                    list_table.append(ls[j])
                
                                else:
                                    break
                                
                                index4 = j
                                j += 1
                                
                        elif ls[i] == 'and' and ls[i + 1] == 'is' and ls[i + 2] == 'not' and (ls[i + 3] == 'on' or ls[i + 3] == 'above' or ls[i + 3] == 'below') and (ls[i + 4] == month or ls[i + 5] == month or ls[i + 6] == month):
                            index9 = i
                            while j < len(ls):
                                if ls[j] != 'table' and ls[j] != 'degree' and ls[j] != 'percent' and ls[j] != 'lux' and ls[j] != 'ppm' and ls[j] != 'temperature' and ls[j] != 'soil' and ls[j] != 'humidity' and ls[j] != 'air' and ls[j] != 'light'and ls[j] != 'table' and ls[j] != 'where' and ls[j] != cmd and ls[j] != 'of':
                                    list_date2.append(ls[j])
                                    ffdate3 = 1
                                    ffdate2 = 1
                                    ffdate = 1
                                else:
                                    break
                                
                                index10 = j
                                j += 1
                                
                        elif not ffdate3 and ls[i] == 'and' and (ls[i + 1] == 'not' or ls[i + 1] == 'is') and (ls[i + 2] == 'on' or ls[i + 2] == 'above' or ls[i + 2] == 'below') and (ls[i + 3] == month or ls[i + 4] == month or ls[i + 5] == month):
                            index9 = i
                            while j < len(ls):
                                if ls[j] != 'table' and ls[j] != 'degree' and ls[j] != 'percent' and ls[j] != 'lux' and ls[j] != 'ppm' and ls[j] != 'temperature' and ls[j] != 'soil' and ls[j] != 'humidity' and ls[j] != 'air' and ls[j] != 'light'and ls[j] != 'table' and ls[j] != 'where' and ls[j] != cmd and ls[j] != 'of':
                                    list_date2.append(ls[j])
                                    
                                    ffdate2 = 1
                                    ffdate = 1
                                else:
                                    break
                                
                                index10 = j
                                j += 1
                        elif not ffdate2 and (ls[i] == 'not' or ls[i] == 'is') and (ls[i + 1] == 'on' or ls[i + 1] == 'above' or ls[i + 1] == 'below') and (ls[i + 2] == month or ls[i + 3] == month or ls[i + 4] == month):
                            index9 = i
                            while j < len(ls):
                                if ls[j] != 'table' and ls[j] != 'degree' and ls[j] != 'percent' and ls[j] != 'lux' and ls[j] != 'ppm' and ls[j] != 'temperature' and ls[j] != 'soil' and ls[j] != 'humidity' and ls[j] != 'air' and ls[j] != 'light'and ls[j] != 'table' and ls[j] != 'where' and ls[j] != cmd and ls[j] != 'of':
                                    list_date2.append(ls[j])
                                    ffdate = 1
                                else:
                                    break
                                
                                index10 = j
                                j += 1
                                
                        elif not ffdate and (ls[i] == 'on' or ls[i] == 'above' or ls[i] == 'below' or  ls[i] == 'and' or ls[i] == 'or') and (ls[i + 1] == month or ls[i + 2] == month or ls[i + 3] == month):
                            index7 = i
                            while j < len(ls):
                                if ls[j] != 'table' and ls[j] != 'degree' and ls[j] != 'percent' and ls[j] != 'lux' and ls[j] != 'ppm' and ls[j] != 'temperature' and ls[j] != 'soil' and ls[j] != 'humidity' and ls[j] != 'air' and ls[j] != 'light'and ls[j] != 'table' and ls[j] != 'where' and ls[j] != cmd and ls[j] != 'of':
                                    list_date2.append(ls[j])
                                else:
                                    break
                                
                                index8 = j
                                j += 1
                                
                        i += 1
            else:
                    i = 0
                    
                    list_cmd = []
                    list_table = []
                    list_condition = []
                    list_date2 = []
                    ffdate = 0
                    ffdate2 = 0
                    ffdate3 = 0
                    
                    while i < len(ls):
                        j = i
                        
                        if ls[i] == cmd:
                            index = i
                            while j < len(ls):
                                if ls[j] != 'of' and ls[j] != 'where' and ls[j] != 'on' and ls[j] != 'above' and ls[j] != 'below' and ls[j] != 'not':
                                    list_cmd.append(ls[j])
                                else:
                                    break
                                
                                index2 = j
                                j += 1

                        elif ls[i] == 'of' and (ls[i + 2] == 'table' or ls[i + 3] == 'table'):
                            index3 = i
                            while j < len(ls):
                                if ls[j] != 'where' and ls[j] != cmd and ls[j] != 'is' and ls[j] != 'not' and ls[j] != 'above' and ls[j] != 'below' and ls[j] != 'equal' and ls[j] != 'on' and ls[j] != 'and' and ls[j] != 'or' and ls[j] != 'on':
                                    list_table.append(ls[j])
                
                                else:
                                    break
                                
                                index4 = j
                                j += 1
                                
                        i += 1
        except:
            None

        r = []
        r2 = []
        r3 = []
        r4 = []
        r5 = []

        try:
            for x in range(index, index2 + 1):
                r.append(x)
            for x in range(index3, index4 + 1):
                r2.append(x)
            for x in range(index6, index5 + 1):
                r3.append(x)
            for x in range(index7, index8 + 1):
                r4.append(x)
            for x in range(index9, index10 + 1):
                r5.append(x)
            

            ran = []
            ran.extend(r)
            ran.extend(r2)
            ran.extend(r3)
            ran.extend(r4)
            ran.extend(r5)
            ran = list(set(ran))
            ran.sort()
            
        except:
            None


        if 0 not in ran:
            ran.insert(0, -1)
            miss = [x for x in range(ran[0], ran[-1] + 1) if x not in ran]
        elif len(ls) - 1 not in ran:
            ran.insert(len(ls) - 1, len(ls))
            miss = [x for x in range(ran[0], ran[-1] + 1) if x not in ran]
        else:
            miss = [x for x in range(ran[0], ran[-1] + 1) if x not in ran]

        miss = list(set(miss))
        miss.sort()

        for x in miss:
            list_condition.append(ls[x])

        if list_condition:
            if 'where' not in list_condition:
                list_condition.insert(0, 'where')

        tokens = []

        tokens = list_cmd.copy()
        tokens.extend(list_table)
        tokens.extend(list_condition)

        if 'today' in ls:
            if 'and' not in list_date and 'or' not in list_date and list_date:
                list_date.insert(0, 'and')
            if 'is' not in list_date and list_date:
                list_date.insert(1, 'is')
                
            tokens.extend(list_date)

        if list_date2:
            if 'not' in list_date2 and 'and' not in list_date2 and 'or' not in list_date2 and list_date2:
                list_date2.insert(list_date2.index('not'), 'and')
            if 'not' in list_date2 and 'and' not in list_date2 and 'or' in list_date2 and list_date2:
                list_date2.insert(list_date2.index('not'), 'and')
            if 'on' not in list_date2 and 'and' in list_date2 and 'or' not in list_date2 and 'above' not in list_date2 and 'below' not in list_date2 and list_date2:
                list_date2.insert(list_date2.index('and') + 1, 'on')
            if 'on' not in list_date2 and 'and' not in list_date2 and 'or' in list_date2 and 'above' not in list_date2 and 'below' not in list_date2 and list_date2:
                list_date2.insert(list_date2.index('or') + 1, 'on')
            if 'on' in list_date2 and 'and' not in list_date2 and 'or' not in list_date2 and list_date2:
                list_date2.insert(0, 'and')
            if 'date' not in list_date2 and 'is'  in list_date2 and 'and' in list_date2 and list_date2:
                list_date2.insert(list_date2.index('is'), 'date')
            if 'date' not in list_date2 and 'is' not in list_date2 and 'and' in list_date2 and list_date2:
                list_date2.insert(list_date2.index('and') + 1, 'date')
                list_date2.insert(list_date2.index('date') + 1, 'is')
            if 'date' not in list_date2 and 'is' not in list_date2 and 'or' in list_date2 and list_date2:
                list_date2.insert(list_date2.index('or') + 1, 'date')
                list_date2.insert(list_date2.index('date') + 1, 'is')


            if ('above' in list_date2 or 'below' in list_date2) and 'and' not in list_date2:
                list_date2.insert(0, 'and')

            tokens.extend(list_date2)

        return tokens

    def check_parameters(self, tokens):
        try: 
            i = 0

            while i < len(tokens):
                j = 0
                
                while j < len(self.params):
                    if self.params[j] == tokens[i]:
                        tokens.insert(i + 1, 'where')
                        tokens.insert(i + 2, 'is')
                    
                    j +=1
                i += 1

            return tokens
        except:
            None

    '''transform input query to cleaner text'''
    def clean_text(self):
        cmd_list = ['show', 'display', 'list', 'get', 'what']
        #convert query to lowercase
        lowercase_query = self.q.lower()

        flag = 0

        if 'table' in lowercase_query or 'plant' in lowercase_query:
            flag = 1
        
        #remove punctuation marks and tokenize
        tokenizer = nltk.RegexpTokenizer(r'\w+')
        tokens = tokenizer.tokenize(lowercase_query)

        tokens = self.arrange_tokens(tokens, cmd_list)
 
        temp = ''

        if flag: 

            i = 0

            while i < len(tokens):
                if tokens[i] == 'plant' or tokens[i] == 'table':
                    temp = tokens[i - 1]
                    break

                i += 1

        cmd_index = 0

        i = 0

        while i < len(cmd_list):
            j = 0

            while j < len(tokens):
                if cmd_list[i] == tokens[j]:
                    cmd_index = j

                j += 1
            i += 1

        splice_cmd = tokens[cmd_index:]
        splice_condition = tokens[:cmd_index]

        tokens = []
        tokens = splice_cmd.copy()

        tokens.extend(splice_condition)


        if self.pff:
            tokens = self.check_parameters(tokens)
        self.save_for_later = tokens.copy()

        temp = ''

        if flag: 

            i = 0

            while i < len(tokens):
                if tokens[i] == 'plant' or tokens[i] == 'table':
                    temp = tokens[i - 1]
                    break

                i += 1

            i = 0

            while i < len(tokens):
                if 'of' == tokens[i]  and (tokens[i + 2] == 'table' or tokens[i + 3] == 'table'):
                    tokens.insert(i, temp)
                    tokens.insert(i + 1, 'plant')
                    tokens.insert(i + 2, 'stop')

                    break

                i += 1

        i = 0

        try:
            tokens.append('stop')
            while tokens[i] != 'stop':
                if tokens[i] == 'and' or tokens[i] == 'or':
                    tokens[i] = ''

                i += 1
        except:
            None

        tokens = list(filter(None, tokens))
        tokens.remove('stop')

        indx = 0

        try:
            indx = tokens.index('below')

            if indx:
                if tokens[indx + 1] == 'or' and tokens[indx + 2] == 'equal':
                    tokens.remove('or')
        except:
            None

        try:
            indx = tokens.index('above')

            if indx:
                if tokens[indx + 1] == 'or' and tokens[indx + 2] == 'equal':
                    tokens.remove('or')
        except:
            None

        try:    
            tokens.remove('stop')
            tokens.remove('stop')
            tokens.remove('stop')
        except:
            None


        tokens = ' '.join(tokens)
        tokens = list(tokens.split(' '))
        
        try:
            i = 0

            while i < len(tokens):
                if tokens[i] == 'and' and tokens[i + 1] == 'is' and tokens[i + 2] == 'and':
                    del tokens[i]
                    del tokens[i]

                i += 1 
        except:
            pass
        
        self.tokens2 = tokens.copy()


        try:
            tokens = tokens[:tokens.index('or')]
        except:
            None

        try:
            tokens = tokens[:tokens.index('and')]
        except:
            None

        i = 0

        while i < len(self.tokens2):
            if 'where' != self.tokens2[i] and 'whose' != self.tokens2[i] and 'that' != self.tokens2[i]:
                self.tokens2[i] = ''
            else:
                break

            i += 1

        i = 0

        while i < len(self.tokens2):
            if 'or' != self.tokens2[i] and 'and' != self.tokens2[i]:
                self.tokens2[i] = ''
            else:
                break

            i += 1

        #remove stop words
        custom_stopwords = stopwords.words('english')
        custom_stopwords.remove('above')
        custom_stopwords.remove('below')
        custom_stopwords.remove('what')
        custom_stopwords.remove('all')
        custom_stopwords.remove('not')
        custom_stopwords.remove('is')
        custom_stopwords.append('quality')
        custom_stopwords.append('level')
        custom_stopwords.append('moisture')
        custom_stopwords.append('equivalent')
        custom_stopwords.append('exactly')
        stopword_tokens = [word for word in tokens if word not in custom_stopwords]

        #lemmatize
        wordnet_lemmatizer = WordNetLemmatizer()
        lemmatized_tokens = [wordnet_lemmatizer.lemmatize(word) for word in stopword_tokens]

        if lemmatized_tokens:
            if lemmatized_tokens[0] == temp:
                lemmatized_tokens[0] = ''
                lemmatized_tokens[1] = ''
                
        #remove stop words
        custom_stopwords = stopwords.words('english')
        custom_stopwords.remove('above')
        custom_stopwords.remove('below')
        custom_stopwords.remove('what')
        custom_stopwords.remove('all')
        custom_stopwords.remove('not')
        custom_stopwords.remove('is')
        custom_stopwords.append('quality')
        custom_stopwords.append('level')
        custom_stopwords.append('moisture')
        custom_stopwords.append('equivalent')
        custom_stopwords.append('exactly')
        custom_stopwords.remove('and')
        custom_stopwords.remove('or')
        self.stopwords2 = [word for word in self.tokens2 if word not in custom_stopwords]

        #lemmatize
        wordnet_lemmatizer = WordNetLemmatizer()
        self.lemmatized_tokens2 = [wordnet_lemmatizer.lemmatize(word) for word in self.stopwords2]

        try:
            i = 0

            while i < len(lemmatized_tokens):
                if lemmatized_tokens[i] == 'is':
                    lemmatized_tokens[i] = ''
                elif lemmatized_tokens[i] == 'and' and lemmatized_tokens[i + 1] == 'and':
                    del lemmatized_tokens[i]

                if temp == lemmatized_tokens[i]:
                    break
                    
                i += 1
        except:
            None

        lemmatized_tokens = [x for x in lemmatized_tokens if x != '']
        lemmatized_tokens = [x for x in lemmatized_tokens if x != 'on']

        return lemmatized_tokens

















