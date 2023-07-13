from msilib.schema import Class
from re import A
from numpy import equal
from classifier import *
import speech_recognition as sr
import re
from datetime import date, datetime, timedelta


class SQLGenerator:
    # def __init__(self, q='', t='', q2='', isOptimum=False, isGraph=False):
    #     self.q = q
    #     self.t = t
    #     self.query = ''
    #     self.err = ''
    #     self.q2 = q2
    #     self.param_err = 0
    #     self.query_flag = 0
    #     self.temp2 = 0
    #     self.sql_schema_tbl = [] 
    #     self.list_sql_multi = []
    #     self.isOptimum = isOptimum
    #     self.isGraph = isGraph

    def __init__(self, q='', q2='', isOptimum=False, isGraph=False):
        self.q = q
        self.query = ''
        self.err = ''
        self.q2 = q2
        self.param_err = 0
        self.query_flag = 0
        self.temp2 = 0
        self.sql_schema_tbl = [] 
        self.list_sql_multi = []
        self.isOptimum = isOptimum
        self.isGraph = isGraph

    def bigram(list_toks): 
        d = zip(*[list_toks[i:] for i in range(0, 2)])
        list_ngrams = [' '.join(n) for n in d]
        
        i = 0
        
        while i < len(list_ngrams):
            if list_ngrams[i] == 'temperature is':
                list_toks.append(list_ngrams[i])
            # elif list_ngrams[i] == 'opt_temperature is':
            #     list_toks.append(list_ngrams[i])
            elif list_ngrams[i] == 'humidity is':
                list_toks.append(list_ngrams[i])
            # elif list_ngrams[i] == 'opt_humidity is':
            #     list_toks.append(list_ngrams[i])
            elif list_ngrams[i] == 'air is':
                list_toks.append(list_ngrams[i])
            elif list_ngrams[i] == 'opt_air is':
                list_toks.append(list_ngrams[i])
            elif list_ngrams[i] == 'soil is':
                list_toks.append(list_ngrams[i])
            # elif list_ngrams[i] == 'opt_soil is':
            #     list_toks.append(list_ngrams[i])
            elif list_ngrams[i] == 'light is':
                list_toks.append(list_ngrams[i])
            elif list_ngrams[i] == 'opt_light is':
                list_toks.append(list_ngrams[i])
            elif list_ngrams[i] == 'table is':
                list_toks.append(list_ngrams[i])
            elif list_ngrams[i] == 'plant is':
                list_toks.append(list_ngrams[i])
            elif list_ngrams[i] == 'going above':
                list_toks.append(list_ngrams[i])
            elif list_ngrams[i] == 'going below':
                list_toks.append(list_ngrams[i])
            elif list_ngrams[i] == 'plant not':
                list_toks.append(list_ngrams[i])
            elif list_ngrams[i] == 'table not':
                list_toks.append(list_ngrams[i])
            elif list_ngrams[i] == 'date is':
                list_toks.append(list_ngrams[i])

            i += 1

        return list_toks

    def add_table_names(self, list_toks):
        i = 0

        while i < len(list_toks):
            if list_toks[i] == 'plant' or list_toks[i] == 'table':
                self.sql_schema_tbl.append(list_toks[i - 1])

            i += 1

        if self.sql_schema_tbl:
            self.sql_schema_tbl = list(set(self.sql_schema_tbl))
            return self.sql_schema_tbl

        return None

    def add_multiple_conditions(self, list_sql_syntax, param, sql_schema, t, param_err):
        self.query_flag = 0
        # self.t = t
        today = datetime.today()
        yesterday = today - timedelta(days = 1)

        param_err = 1
        temp = list_sql_syntax.copy()
        sub_sql_list = []

        self.q2 = list(filter(None, self.q2))

        i = 0

        while i < len(self.q2):
            if 'equal' == self.q2[i]:
                try:
                    if i > 0:
                        if 'or' == self.q2[i - 1]:
                            del self.q2[i - 1]
                except:
                    None

            i += 1
    
        i = 0

        while i < len(self.q2):
            if 'and' == self.q2[i]:
                temp.append('AND') 

            elif 'or' == self.q2[i]:
                temp.append('OR')
            else:
                sub_sql_list.append(self.q2[i])

                try:
                    if  i == len(self.q2) - 1 or self.q2[i + 1] == 'and' or self.q2[i + 1] == 'or':

                        param = j = 0

                        while j < len(sub_sql_list):
                            if sub_sql_list[j] == 'degree' or sub_sql_list[j] == 'percent' or sub_sql_list[j] == 'ppm' or sub_sql_list[j] == 'lux':
                                param = sub_sql_list[j]

                            j += 1

                        val_cpy = sub_sql_list.copy()
                        # cls3 = Classifier(sub_sql_list, 1, param, sql_schema, self.t, param_err)
                        cls3 = Classifier(sub_sql_list, 1, param, sql_schema, param_err)

                        sql_check = ''
                        sql_check = cls3.ngram_check(self.isGraph)
                        self.temp2 = sql_check
                        
                        if sql_check == 1:
                            self.query_flag = 0
                            temp.append('temperature >=')
                        elif sql_check == 2:
                            self.query_flag = 0
                            temp.append('temperature <=')
                        elif sql_check == 3:
                            self.query_flag = 0
                            temp.append('humidity >=')
                        elif sql_check == 4:
                            self.query_flag = 0
                            temp.append('humidity <=')
                        elif sql_check == 5:
                            self.query_flag = 0
                            temp.append('temperature =')
                        elif sql_check == 6:
                            self.query_flag = 0
                            temp.append('humidity =')
                        elif sql_check == 7:
                            self.query_flag = 0
                            temp.append('temperature >')
                        elif sql_check == 8:
                            self.query_flag = 0
                            temp.append('temperature <')
                        elif sql_check == 9:
                            self.query_flag = 0
                            temp.append('temperature !=')
                        elif sql_check == 10:
                            self.query_flag = 0
                            temp.append('humidity >')
                        elif sql_check == 11:
                            self.query_flag = 0
                            temp.append('humidity <')
                        elif sql_check == 12:
                            self.query_flag = 0
                            temp.append('humidity !=')
                        elif sql_check == 13:
                            self.query_flag = 0
                            temp.append('air =')
                        elif sql_check == 14:
                            self.query_flag = 0
                            temp.append('air >')
                        elif sql_check == 15:
                            self.query_flag = 0
                            temp.append('air <')
                        elif sql_check == 16:
                            self.query_flag = 0
                            temp.append('air !=')
                        elif sql_check == 17:
                            self.query_flag = 0
                            temp.append('air >=')
                        elif sql_check == 18:
                            self.query_flag = 0
                            temp.append('air <=')
                        elif sql_check == 19:
                            self.query_flag = 0
                            temp.append('light =')
                        elif sql_check == 20:
                            self.query_flag = 0
                            temp.append('light >')
                        elif sql_check == 21:
                            self.query_flag = 0
                            temp.append('light <')
                        elif sql_check == 22:
                            self.query_flag = 0
                            temp.append('light !=')
                        elif sql_check == 23:
                            self.query_flag = 0
                            temp.append('light >=')
                        elif sql_check == 24:
                            self.query_flag = 0
                            temp.append('light <=')
                        elif sql_check == 25:
                            self.query_flag = 0
                            temp.append('soil =')
                        elif sql_check == 26:
                            self.query_flag = 0
                            temp.append('soil >')
                        elif sql_check == 27:
                            self.query_flag = 0
                            temp.append('soil <')
                        elif sql_check == 28:
                            self.query_flag = 0
                            temp.append('soil !=')
                        elif sql_check == 29:
                            self.query_flag = 0
                            temp.append('soil >=')
                        elif sql_check == 30:
                            self.query_flag = 0
                            temp.append('soil <=')
                        elif sql_check == 31:
                            self.query_flag = 0
                            temp.append('date =')
                        elif sql_check == 32:
                            self.query_flag = 0
                            temp.append('date >')
                        elif sql_check == 33:
                            self.query_flag = 0
                            temp.append('date <')
                        elif sql_check == 34:
                            self.query_flag = 0
                            temp.append('date !=')
                        elif sql_check == 35:
                            self.query_flag = 0
                            temp.append('date >=')
                        elif sql_check == 36:
                            self.query_flag = 0
                            temp.append('date <=')
                        # elif sql_check == 37:
                        #     self.query_flag = 0
                        #     temp.append('opt_temperature =')
                        # elif sql_check == 38:
                        #     self.query_flag = 0
                        #     temp.append('opt_temperature >')
                        # elif sql_check == 39:
                        #     self.query_flag = 0
                        #     temp.append('opt_temperature <')
                        # elif sql_check == 40:
                        #     self.query_flag = 0
                        #     temp.append('opt_temperature !=')
                        # elif sql_check == 41:
                        #     self.query_flag = 0
                        #     temp.append('opt_temperature >=')
                        # elif sql_check == 42:
                        #     self.query_flag = 0
                        #     temp.append('opt_temperature <=')
                        # elif sql_check == 43:
                        #     self.query_flag = 0
                        #     temp.append('opt_humidity =')
                        # elif sql_check == 44:
                        #     self.query_flag = 0
                        #     temp.append('opt_humidity >')
                        # elif sql_check == 45:
                        #     self.query_flag = 0
                        #     temp.append('opt_humidity <')
                        # elif sql_check == 46:
                        #     self.query_flag = 0
                        #     temp.append('opt_humidity !=')
                        # elif sql_check == 47:
                        #     self.query_flag = 0
                        #     temp.append('opt_humidity >=')
                        # elif sql_check == 48:
                        #     self.query_flag = 0
                        #     temp.append('opt_humidity <=')
                        # elif sql_check == 49:
                        #     self.query_flag = 0
                        #     temp.append('opt_soil =')
                        # elif sql_check == 50:
                        #     self.query_flag = 0
                        #     temp.append('opt_soil >')
                        # elif sql_check == 51:
                        #     self.query_flag = 0
                        #     temp.append('opt_soil <')
                        # elif sql_check == 52:
                        #     self.query_flag = 0
                        #     temp.append('opt_soil !=')
                        # elif sql_check == 53:
                        #     self.query_flag = 0
                        #     temp.append('opt_soil >=')
                        # elif sql_check == 54:
                        #     self.query_flag = 0
                        #     temp.append('opt_soil <=')
                        elif sql_check == 55:
                            self.query_flag = 0
                            temp.append('opt_light =')
                        elif sql_check == 56:
                            self.query_flag = 0
                            temp.append('opt_light >')
                        elif sql_check == 57:
                            self.query_flag = 0
                            temp.append('opt_light <')
                        elif sql_check == 58:
                            self.query_flag = 0
                            temp.append('opt_light !=')
                        elif sql_check == 59:
                            self.query_flag = 0
                            temp.append('opt_light >=')
                        elif sql_check == 60:
                            self.query_flag = 0
                            temp.append('opt_light <=')
                        elif sql_check == 61:
                            self.query_flag = 0
                            temp.append('opt_air =')
                        elif sql_check == 62:
                            self.query_flag = 0
                            temp.append('opt_air >')
                        elif sql_check == 63:
                            self.query_flag = 0
                            temp.append('opt_air <')
                        elif sql_check == 64:
                            self.query_flag = 0
                            temp.append('opt_air !=')
                        elif sql_check == 65:
                            self.query_flag = 0
                            temp.append('opt_air >=')
                        elif sql_check == 66:
                            self.query_flag = 0
                            temp.append('opt_air <=')
                        elif sql_check < 0:
                            self.query_flag = 1
                            self.temp2 = sql_check

                        if not self.query_flag and sql_check > 0 :
                            month = ''
                            d = ''
                            y = ''
                            day = ''
                            year = ''

                            for key in self.month_list:
                                z = 0
                                
                                while z < len(val_cpy):
                                    if key == val_cpy[z]:
                                        month = self.month_list[key]
                                        break

                                    z += 1

                            date_list = []

                            if 'today' in val_cpy:
                                temp.append(today.strftime("'%Y-%m-%d'"))
                            elif 'yesterday' in val_cpy:
                                temp.append(yesterday.strftime("'%Y-%m-%d'"))
                            elif month:
                                try:
                                    d = [e for e in val_cpy if e.isnumeric() if  32 > int(e) > 0]
                                    y = [e for e in val_cpy if e.isnumeric() if 3000 > int(e) > 1999]
                                    day = d[0].lstrip('0')
                                    year = y[0].lstrip('0')
                                except:
                                    None
                            
                                if year and day:
                                    try:
                                        date_list.append(year)
                                        date_list.append(month.zfill(2))
                                        date_list.append(day.zfill(2))
                                        str_date = "'" + '-'.join(date_list) + "'"
                                        temp.append(str_date)
                                    except:
                                        None
                                else:
                                    self.query_flag = 1
                                    return '-4'
                            else:
                                for x in val_cpy:
                                    try:
                                        int(x)
                                        self.query_flag = 0
                                        temp.append(x)
                                        
                                        break
                                    except:
                                        self.query_flag = 1

                                if 'date' in ' '.join(sub_sql_list):
                                    self.query_flag = 1
                                    return '-4'    
                            
                            sub_sql_list = []
                except:
                    None
            i += 1

        return temp

    '''generate sql query via user-defined algorithm'''
    def generate_sql_statement(self):
        '''replace query with sql keywords and append unmatched items to a list'''
        list_tokens = self.q
        list_temp_tokens = []
        self.year_list = list(range(2000, 2023))
        self.month_list = {
            'january': '1', 
            'february': '2', 
            'march': '3', 
            'april': '4', 
            'may': '5', 
            'june': '6', 
            'july': '7', 
            'august': '8', 
            'september': '9', 
            'october': '10', 
            'november': '11', 
            'december': '12'
            }
        self.days_list = list(range(1, 32))


        # sql_schema = [['temperature', 'humidity', 'air', 'soil', 'light', 'date', 'opt_temperature', 'opt_humidity', 'opt_soil', 'opt_light', 'opt_air'], ['']]
        sql_schema = [['temperature', 'humidity', 'air', 'soil', 'light', 'date', 'opt_light', 'opt_air'], ['']]

        temp = 0
        # cls = Classifier(list_tokens, 0, 0, sql_schema, self.t)
        cls = Classifier(list_tokens, 0, 0, sql_schema)
        temp = cls.ngram_check(self.isGraph)

        num_err = re.sub('\d', 'x', ' '.join(list_tokens))

        if 'temperature x' in num_err:
            self.err = 'Sorry I am having some trouble understanding your query please try again'
            return self.err
        # if 'opt_temperature x' in num_err:
        #     self.err = 'Sorry I am having some trouble understanding your query please try again'
        #     return self.err
        if 'humidity x' in num_err:
            self.err = 'Sorry I am having some trouble understanding your query please try again'
            return self.err
        # if 'opt_humidity x' in num_err:
        #     self.err = 'Sorry I am having some trouble understanding your query please try again'
        #     return self.err
        if 'air x' in num_err:
            self.err = 'Sorry I am having some trouble understanding your query please try again'
            return self.err
        if 'opt_air x' in num_err:
            self.err = 'Sorry I am having some trouble understanding your query please try again'
            return self.err
        if 'light x' in num_err:
            self.err = 'Sorry I am having some trouble understanding your query please try again'
            return self.err
        if 'opt_light x' in num_err:
            self.err = 'Sorry I am having some trouble understanding your query please try again'
            return self.err
        if 'soil x' in num_err:
            self.err = 'Sorry I am having some trouble understanding your query please try again'
            return self.err
        # if 'opt_soil x' in num_err:
        #     self.err = 'Sorry I am having some trouble understanding your query please try again'
        #     return self.err
        if 'date x' in num_err:
            self.err = 'Sorry I am having some trouble understanding your query please try again'
            return self.err

        add_WHERE_cond = re.sub(r'is|not|above|below|equal', 'y',' '.join(list_tokens))

        sql_keywords = {
            'show': 'SELECT',
            'display': 'SELECT',
            'list': 'SELECT',
            'get': 'SELECT',
            'what': 'SELECT',
            'plant': 'FROM',
            'table': 'FROM',
            'degree': 'WHERE',
            'percent': 'WHERE',
            'ppm': 'WHERE',
            'lux': 'WHERE',
            'temperature is': 'WHERE',
            # 'opt_temperature is': 'WHERE',
            'humidity is': 'WHERE',
            # 'opt_humidity is': 'WHERE',
            'air is': 'WHERE',
            'opt_air is': 'WHERE',
            'soil is': 'WHERE',
            # 'opt_soil is': 'WHERE',
            'date is': 'WHERE',
            'light is': 'WHERE',
            'opt_light is': 'WHERE',
            'table is': 'WHERE',
            'plant is': 'WHERE',
            'plant not': 'WHERE',
            'table not': 'WHERE',
            'going': 'WHERE',
            'going above': 'WHERE',
            'going below': 'WHERE'
        }

        list_tokens = SQLGenerator.bigram(list_tokens)

        sql_schema[1] = self.add_table_names(list_tokens)
        
        try:
            sql_schema[1] = [i for i in sql_schema[1] if i]
        except:
            None

        param = i = 0

        while i < len(list_tokens):
            flag = 0

            for key in sql_keywords:
                if key == list_tokens[i]:
                    if key == 'degree' or key == 'percent' or key == 'ppm' or key == 'lux':
                        param = key
                        
                    flag = 1
                    list_tokens[i] = sql_keywords[key]
                    break

            if not flag:
                list_temp_tokens.append(list_tokens[i])
                list_tokens.pop(i)

                i -= 1

            i += 1

        if 'temperature y' in add_WHERE_cond:
                list_tokens.append('WHERE')
        if 'humidity y' in add_WHERE_cond:
                list_tokens.append('WHERE')
        if 'air y' in add_WHERE_cond:
                list_tokens.append('WHERE')
        if 'light y' in add_WHERE_cond:
                list_tokens.append('WHERE')
        if 'soil y' in add_WHERE_cond:
                list_tokens.append('WHERE')
        if 'date y' in add_WHERE_cond:
                list_tokens.append('WHERE')
        # if 'opt_temperature y' in add_WHERE_cond:
        #     list_tokens.append('WHERE')
        # if 'opt_humidity y' in add_WHERE_cond:
        #     list_tokens.append('WHERE')
        # if 'opt_soil y' in add_WHERE_cond:
        #     list_tokens.append('WHERE')
        if 'opt_light y' in add_WHERE_cond:
            list_tokens.append('WHERE')
        if 'opt_air y' in add_WHERE_cond:
            list_tokens.append('WHERE')

        #remove sql keyword redundancies
        list_tokens = list(set(list_tokens)) 

        '''rearrange list items into SQL syntax'''
        list_sql_syntax = [0] * 3

        i = 0

        while i < len(list_tokens):
            if list_tokens[i] == 'SELECT':
                list_sql_syntax[0] = list_tokens[i]
            elif list_tokens[i] == 'FROM':
                list_sql_syntax[1] = list_tokens[i]
            else:
                list_sql_syntax[2] = list_tokens[i]
            
            i += 1

        #remove zeroes in list
        list_sql_syntax[:] = (v for v in list_sql_syntax if v != 0) 

        '''map list items with user-defined schema'''    
        temp2 = 0
        # cls2 = Classifier(list_temp_tokens, 1, param, sql_schema, self.t)
        cls2 = Classifier(list_temp_tokens, 1, param, sql_schema)
        temp2 = cls2.ngram_check(self.isGraph)
        
        sql_flag = 0

        humidity_or_soil = 0

        sql_condition = {}
        
        if not temp2: 
            if param == 'degree':
                sql_condition = {
                    'above': 'temperature >',
                    'below': 'temperature <',
                    'is': 'temperature =',
                    'not': 'temperature !='
                }
            elif param == 'percent':

                # self.t.say('Please choose one between humidity level or soil moisture')
                # self.t.runAndWait()

                r = sr.Recognizer()
                with sr.Microphone() as source: 

                    # self.t.say('Say humidity, to obtain the humidity level or say soil for soil moisture')
                    # self.t.runAndWait()
                    # self.t.stop()

                    audio = r.listen(source)

                    try:
                        humidity_or_soil = r.recognize_google(audio)    

                        # self.t.say('You said')
                        # self.t.runAndWait()
                        # self.t.say(humidity_or_soil)
                        # self.t.runAndWait()
                    except:
                        temp2 = -1
                
                if humidity_or_soil == 'humidity':
                    sql_condition = {
                        'above': 'humidity >',
                        'below': 'humidity <',
                        'is': 'humidity =',
                        'not': 'humidity !='
                    }
                elif humidity_or_soil == 'soil':
                    sql_condition = {
                        'above': 'soil >',
                        'below': 'soil <',
                        'is': 'soil =',
                        'not': 'soil !='
                    }
                else:
                    sql_flag = 1
            elif param == 'ppm':
                sql_condition = {
                    'above': 'air >',
                    'below': 'air <',
                    'is': 'air =',
                    'not': 'air !='
                }
            elif param == 'lux':
                sql_condition = {
                    'above': 'light >',
                    'below': 'light <',
                    'is': 'light =',
                    'not': 'light !='
                }

        if not sql_flag:
            i = 0
            
            if 'SELECT' == ' '.join(list_sql_syntax):
                join_tbl_list = []
                
                while i < len(list_temp_tokens):        
                    j = 0
                        
                    while j < len(sql_schema[0]):
                        if list_temp_tokens[i] == 'all':
                            sql_flag = 0
                            list_sql_syntax.append('*')

                        elif list_temp_tokens[i] == sql_schema[0][j]:
                            sql_flag = 0
                            join_tbl_list.append(sql_schema[0][j])
                        
                        j += 1
                    i += 1

                if len(join_tbl_list):
                    try:
                        list_sql_syntax = [x for x in list_sql_syntax if x != '']
                    except:
                        None
                    try:
                        list_sql_syntax = [x for x in list_sql_syntax if x != '*']
                    except:
                        None
                
                if list_sql_syntax.count('*') > 1:
                    seen = set()
                    seen_add = seen.add
                    list_sql_syntax = [x for x in list_sql_syntax if not (x in seen or seen_add(x))]

                join_sql_tbl_str = ', '.join(join_tbl_list)
                list_sql_syntax.insert(1, join_sql_tbl_str)
            elif 'SELECT FROM' == ' '.join(list_sql_syntax):
                flag = flag2 = 0
                
                while i < len(list_temp_tokens):
                    j = 0

                    if not flag:
                        while j < len(sql_schema[0]):
                            if isinstance(temp, str):
                                flag = 1
                                list_sql_syntax.insert(1, temp)

                                break
                            elif temp == 1:
                                flag = 1
                                list_sql_syntax.insert(1, 'temperature')

                                break
                            elif temp == 2:
                                flag = 1
                                list_sql_syntax.insert(1, 'humidity')

                                break
                            elif temp == 3:
                                flag = 1
                                list_sql_syntax.insert(1, 'air')

                                break
                            elif temp == 4:
                                flag = 1
                                list_sql_syntax.insert(1, 'soil')

                                break
                            elif temp == 5:
                                flag = 1
                                list_sql_syntax.insert(1, 'light')

                                break
                            elif temp == 6:
                                flag = 1
                                list_sql_syntax.insert(1, 'date')

                                break
                            # elif temp == 7:
                            #     flag = 1
                            #     list_sql_syntax.insert(1, 'opt_temperature')

                            #     break
                            # elif temp == 8:
                            #     flag = 1
                            #     list_sql_syntax.insert(1, 'opt_humidity')

                            #     break
                            # elif temp == 9:
                            #     flag = 1
                            #     list_sql_syntax.insert(1, 'opt_soil')

                            #     break
                            elif temp == 10:
                                flag = 1
                                list_sql_syntax.insert(1, 'opt_light')

                                break
                            elif temp == 11:
                                flag = 1
                                list_sql_syntax.insert(1, 'opt_air')

                                break
                            elif list_temp_tokens[i] == 'all' or list_temp_tokens[i] == 'reading':
                                flag = 1
                                list_sql_syntax.insert(1, '*')

                                break
                            elif list_temp_tokens[i] == sql_schema[0][j]:
                                flag = 1
                                list_sql_syntax.insert(1, sql_schema[0][j])

                                break
                            
                            j += 1
                
                    j = 0
                
                    if not flag2:
                        join_tbl_list = []
                        
                        while j < len(sql_schema[1]):
                            if sql_schema[1][j] == 'dummy':
                                flag2 = 1
                                join_tbl_list.append('dummy')
                            else:
                                flag2 = 1
                                join_tbl_list.append(sql_schema[1][j] + '_table')
                            
                            j += 1

                        join_sql_tbl_str = ', '.join(join_tbl_list)
                        list_sql_syntax.insert(3, join_sql_tbl_str)

                    if flag and flag2:
                        sql_flag = 0

                        break
                        
                    i += 1
            elif 'SELECT FROM WHERE' == ' '.join(list_sql_syntax):
                flag = flag2 = 0
                
                while i < len(list_temp_tokens):
                    j = 0

                    if not flag:
                        while j < len(sql_schema[0]):
                            if isinstance(temp, str):
                                flag = 1
                                list_sql_syntax.insert(1, temp)

                                break
                            elif temp == 1:
                                flag = 1
                                list_sql_syntax.insert(1, 'temperature')

                                break
                            elif temp == 2:
                                flag = 1
                                list_sql_syntax.insert(1, 'humidity')

                                break
                            elif temp == 3:
                                flag = 1
                                list_sql_syntax.insert(1, 'air')

                                break
                            elif temp == 4:
                                flag = 1
                                list_sql_syntax.insert(1, 'soil')

                                break
                            elif temp == 5:
                                flag = 1
                                list_sql_syntax.insert(1, 'light')

                                break
                            elif temp == 6:
                                flag = 1
                                list_sql_syntax.insert(1, 'date')

                                break
                            # elif temp == 7:
                            #     flag = 1
                            #     list_sql_syntax.insert(1, 'opt_temperature')

                            #     break
                            # elif temp == 8:
                            #     flag = 1
                            #     list_sql_syntax.insert(1, 'opt_humidity')

                            #     break
                            # elif temp == 9:
                            #     flag = 1
                            #     list_sql_syntax.insert(1, 'opt_soil')

                            #     break
                            elif temp == 10:
                                flag = 1
                                list_sql_syntax.insert(1, 'opt_light')

                                break
                            elif temp == 11:
                                flag = 1
                                list_sql_syntax.insert(1, 'opt_air')

                                break
                            elif list_temp_tokens[i] == 'all' or list_temp_tokens[i] == 'reading':
                                flag = 1
                                list_sql_syntax.insert(1, '*')

                                break
                            elif list_temp_tokens[i] == sql_schema[0][j]:
                                flag = 1
                                list_sql_syntax.insert(1, sql_schema[0][j])

                                break
                            
                            j += 1
                
                    j = 0
                
                    if not flag2:
                        join_tbl_list = []

                        while j < len(sql_schema[1]):
                            if sql_schema[1][j] == 'dummy':
                                flag2 = 1
                                join_tbl_list.append('dummy')
                            else:
                                flag2 = 1
                                join_tbl_list.append(sql_schema[1][j] + '_table')
                            
                            j += 1

                        join_sql_tbl_str = ', '.join(join_tbl_list)
                        list_sql_syntax.insert(3, join_sql_tbl_str)

                    if flag and flag2:
                        break
                        
                    i += 1

                if temp2 == 1:
                    sql_flag = 0
                    list_sql_syntax.append('temperature >=')
                elif temp2 == 2:
                    sql_flag = 0
                    list_sql_syntax.append('temperature <=')
                elif temp2 == 3:
                    sql_flag = 0
                    list_sql_syntax.append('humidity >=')
                elif temp2 == 4:
                    sql_flag = 0
                    list_sql_syntax.append('humidity <=')
                elif temp2 == 5:
                    sql_flag = 0
                    list_sql_syntax.append('temperature =')
                elif temp2 == 6:
                    sql_flag = 0
                    list_sql_syntax.append('humidity =')
                elif temp2 == 7:
                    sql_flag = 0
                    list_sql_syntax.append('temperature >')
                elif temp2 == 8:
                    sql_flag = 0
                    list_sql_syntax.append('temperature <')
                elif temp2 == 9:
                    sql_flag = 0
                    list_sql_syntax.append('temperature !=')
                elif temp2 == 10:
                    sql_flag = 0
                    list_sql_syntax.append('humidity >')
                elif temp2 == 11:
                    sql_flag = 0
                    list_sql_syntax.append('humidity <')
                elif temp2 == 12:
                    sql_flag = 0
                    list_sql_syntax.append('humidity !=')
                elif temp2 == 13:
                    sql_flag = 0
                    list_sql_syntax.append('air =')
                elif temp2 == 14:
                    sql_flag = 0
                    list_sql_syntax.append('air >')
                elif temp2 == 15:
                    sql_flag = 0
                    list_sql_syntax.append('air <')
                elif temp2 == 16:
                    sql_flag = 0
                    list_sql_syntax.append('air !=')
                elif temp2 == 17:
                    sql_flag = 0
                    list_sql_syntax.append('air >=')
                elif temp2 == 18:
                    sql_flag = 0
                    list_sql_syntax.append('air <=')
                elif temp2 == 19:
                    sql_flag = 0
                    list_sql_syntax.append('light =')
                elif temp2 == 20:
                    sql_flag = 0
                    list_sql_syntax.append('light >')
                elif temp2 == 21:
                    sql_flag = 0
                    list_sql_syntax.append('light <')
                elif temp2 == 22:
                    sql_flag = 0
                    list_sql_syntax.append('light !=')
                elif temp2 == 23:
                    sql_flag = 0
                    list_sql_syntax.append('light >=')
                elif temp2 == 24:
                    sql_flag = 0
                    list_sql_syntax.append('light <=')
                elif temp2 == 25:
                    sql_flag = 0
                    list_sql_syntax.append('soil =')
                elif temp2 == 26:
                    sql_flag = 0
                    list_sql_syntax.append('soil >')
                elif temp2 == 27:
                    sql_flag = 0
                    list_sql_syntax.append('soil <')
                elif temp2 == 28:
                    sql_flag = 0
                    list_sql_syntax.append('soil !=')
                elif temp2 == 29:
                    sql_flag = 0
                    list_sql_syntax.append('soil >=')
                elif temp2 == 30:
                    sql_flag = 0
                    list_sql_syntax.append('soil <=')
                elif temp2 == 31:
                    sql_flag = 0
                    list_sql_syntax.append('date =')
                elif temp2 == 32:
                    sql_flag = 0
                    list_sql_syntax.append('date >')
                elif temp2 == 33:
                    sql_flag = 0
                    list_sql_syntax.append('date <')
                elif temp2 == 34:
                    sql_flag = 0
                    list_sql_syntax.append('date !=')
                elif temp2 == 35:
                    sql_flag = 0
                    list_sql_syntax.append('date >=')
                elif temp2 == 36:
                    sql_flag = 0
                    list_sql_syntax.append('date <=')
                # elif temp2 == 37:
                #     sql_flag = 0
                #     list_sql_syntax.append('opt_temperature =')
                # elif temp2 == 38:
                #     sql_flag = 0
                #     list_sql_syntax.append('opt_temperature >')
                # elif temp2 == 39:
                #     sql_flag = 0
                #     list_sql_syntax.append('opt_temperature <')
                # elif temp2 == 40:
                #     sql_flag = 0
                #     list_sql_syntax.append('opt_temperature !=')
                # elif temp2 == 41:
                #     sql_flag = 0
                #     list_sql_syntax.append('opt_temperature >=')
                # elif temp2 == 42:
                #     sql_flag = 0
                #     list_sql_syntax.append('opt_temperature <=')
                # elif temp2 == 43:
                #     sql_flag = 0
                #     list_sql_syntax.append('opt_humidity =')
                # elif temp2 == 44:
                #     sql_flag = 0
                #     list_sql_syntax.append('opt_humidity >')
                # elif temp2 == 45:
                #     sql_flag = 0
                #     list_sql_syntax.append('opt_humidity <')
                # elif temp2 == 46:
                #     sql_flag = 0
                #     list_sql_syntax.append('opt_humidity !=')
                # elif temp2 == 47:
                #     sql_flag = 0
                #     list_sql_syntax.append('opt_humidity >=')
                # elif temp2 == 48:
                #     sql_flag = 0
                #     list_sql_syntax.append('opt_humidity <=')
                # elif temp2 == 49:
                #     sql_flag = 0
                #     list_sql_syntax.append('opt_soil =')
                # elif temp2 == 50:
                #     sql_flag = 0
                #     list_sql_syntax.append('opt_soil >')
                # elif temp2 == 51:
                #     sql_flag = 0
                #     list_sql_syntax.append('opt_soil <')
                # elif temp2 == 52:
                #     sql_flag = 0
                #     list_sql_syntax.append('opt_soil !=')
                # elif temp2 == 53:
                #     sql_flag = 0
                #     list_sql_syntax.append('opt_soil >=')
                # elif temp2 == 54:
                #     sql_flag = 0
                #     list_sql_syntax.append('opt_soil <=')
                elif temp2 == 55:
                    sql_flag = 0
                    list_sql_syntax.append('opt_light =')
                elif temp2 == 56:
                    sql_flag = 0
                    list_sql_syntax.append('opt_light >')
                elif temp2 == 57:
                    sql_flag = 0
                    list_sql_syntax.append('opt_light <')
                elif temp2 == 58:
                    sql_flag = 0
                    list_sql_syntax.append('opt_light !=')
                elif temp2 == 59:
                    sql_flag = 0
                    list_sql_syntax.append('opt_light >=')
                elif temp2 == 60:
                    sql_flag = 0
                    list_sql_syntax.append('opt_light <=')
                elif temp2 == 61:
                    sql_flag = 0
                    list_sql_syntax.append('opt_air =')
                elif temp2 == 62:
                    sql_flag = 0
                    list_sql_syntax.append('opt_air >')
                elif temp2 == 63:
                    sql_flag = 0
                    list_sql_syntax.append('opt_air <')
                elif temp2 == 64:
                    sql_flag = 0
                    list_sql_syntax.append('opt_air !=')
                elif temp2 == 65:
                    sql_flag = 0
                    list_sql_syntax.append('opt_air >=')
                elif temp2 == 66:
                    sql_flag = 0
                    list_sql_syntax.append('opt_air <=')
                elif temp2 < 0:
                    sql_flag = 1
                else:
                    if not sql_flag:
                        i = 0

                        while i < len(list_temp_tokens):
                            flag = 0

                            for key in sql_condition:
                                if key == list_temp_tokens[i]:
                                    flag = 1
                                    list_sql_syntax.append(sql_condition[key])

                                    break
                            
                            if flag:
                                sql_flag = 0

                                break

                            i += 1

                if not sql_flag:
                    month = ''
                    d = ''
                    y = ''
                    day = ''
                    year = ''
                    today = datetime.today()
                    yesterday = today - timedelta(days = 1)
                    str_date = ''

                    for key in self.month_list:
                        i = 0
                        
                        while i < len(list_temp_tokens):
                            if key == list_temp_tokens[i]:
                                month = self.month_list[key]
                                break

                            i += 1

                    date_list = []

                    if 'today' in list_temp_tokens:
                        list_sql_syntax.append(today.strftime("'%Y-%m-%d'"))
                    elif 'yesterday' in list_temp_tokens:
                        list_sql_syntax.append(yesterday.strftime("'%Y-%m-%d'"))
                    elif month:
                        try:
                            d = [i for i in list_temp_tokens if i.isnumeric() if  32 > int(i) > 0]
                            y = [i for i in list_temp_tokens if i.isnumeric() if 2023 > int(i) > 1999]
                            day = d[0].lstrip('0')
                            year = y[0].lstrip('0')
                        except:
                            None
                    
                        if year and day:
                            try:
                                date_list.append(year)
                                date_list.append(month.zfill(2))
                                date_list.append(day.zfill(2))

                                str_date = "'" + '-'.join(date_list) + "'"
                                list_sql_syntax.append(str_date)
                            except:
                                None
                        else:
                            sql_flag = 1
                            return '-4'
                    else:
                        for i in list_temp_tokens:
                            try:
                                int(i)
                                sql_flag = 0
                                list_sql_syntax.append(i)
                                
                                break
                            except:
                                sql_flag = 1

                        str_f = ''
                        str_f = re.sub("\d", "x", ' '.join(list_sql_syntax))


                        if 'WHERE x' in str_f:
                            return '-5'

                        if ('date =' in ' '.join(list_sql_syntax) or 'date !=' in ' '.join(list_sql_syntax) or 'date >=' in ' '.join(list_sql_syntax) or 'date <=' in ' '.join(list_sql_syntax)
                        or 'date >' in ' '.join(list_sql_syntax) or 'date <' in ' '.join(list_sql_syntax)):
                            sql_flag = 1
                            return '-4'    
            else:
                sql_flag = 1
        

        temp = zip(*[list_sql_syntax[i:] for i in range(0, 2)])
        list_ngrams = [' '.join(n) for n in temp]

        
        str_flag = ''
        str_flag = re.sub("\d", "x", ' '.join(list_sql_syntax))

        if 'SELECT' == str_flag or 'WHERE x' in str_flag or 'SELECT FROM' in str_flag:
            sql_flag = 1
            temp2 = -3
            
        if not sql_flag:

            sql_query = ' '

            if self.q2: 
                # list_sql_syntax_multi = self.add_multiple_conditions(list_sql_syntax, param, sql_schema, self.t, self.param_err)
                list_sql_syntax_multi = self.add_multiple_conditions(list_sql_syntax, param, sql_schema, self.param_err)

                try:
                    i = 0

                    while i < len(list_sql_syntax_multi):
                        if list_sql_syntax_multi[i] == 'AND' and list_sql_syntax_multi[i + 1] == 'AND':
                            del list_sql_syntax_multi[i]

                            break
                            
                        i += 1
                except:
                    None

                if (list_sql_syntax_multi[-1] == 'OR' or list_sql_syntax_multi[-1] == 'AND') and self.temp2 != -1:
                    self.query_flag = 1
                    self.temp2 = -3

                if 'AND AND' in ' '.join(list_sql_syntax_multi) or 'OR AND' in ' '.join(list_sql_syntax_multi) or 'OR OR' in ' '.join(list_sql_syntax_multi) or 'AND OR' in ' '.join(list_sql_syntax_multi):
                    self.query_flag = 1
                    self.temp2 = -3

                if self.query_flag:
                    if self.temp2 == -1:
                        self.err = 'Failed to generate SQL statement parameter unit is invalid'

                    elif self.temp2 == -2:
                        self.err = 'Failed to generate SQL statement voice is unrecognizable'

                    elif self.temp2 == -3:
                        self.err = 'Sorry I am having some trouble understanding your query please try again'
                    
                    else:
                        self.err = 'Failed to generate SQL statement date is invalid'

                    return self.err

                sql_tts_query = sql_query.join(list_sql_syntax_multi)
                self.query = sql_tts_query
            else:
                sql_tts_query = sql_query.join(list_sql_syntax)
                self.query = sql_tts_query

            dict_chars_replace = {',': ' comma', '>=': 'greater than or equal', '>': 'greater than', '<=': 'less than or equal', 
            '<': 'less than', '!=': 'not equal', '=': 'equal', '-': 'hyphen', "'": 'apostrophe'}

            if (self.isOptimum):
                if "date" in sql_tts_query:
                    sql_tts_query = sql_tts_query.replace("AND", "WHERE", 1)
                    sql_tts_query = sql_tts_query.replace("OR", "WHERE", 1)

            for key, value in dict_chars_replace.items():
                sql_tts_query = sql_tts_query.replace(key, value)

            sql_tts_query = re.sub(r'\bdate\b', 'Date_n_Time', sql_tts_query)
            sql_tts_query = re.sub(r'\btemperature\b', 'Temperature', sql_tts_query)
            sql_tts_query = re.sub(r'\bhumidity\b', 'Humidity', sql_tts_query)
            sql_tts_query = re.sub(r'\blight\b', 'Light_Intensity', sql_tts_query)
            sql_tts_query = re.sub(r'\bsoil\b', 'Soil_Moisture', sql_tts_query)
            sql_tts_query = re.sub(r'\bair\b', 'Air_Quality', sql_tts_query)

            sql_tts_query = re.sub(r'\btomato_table\b', '`sensor_node_1_tb`', sql_tts_query)
            sql_tts_query = re.sub(r'\bgrape_table\b', '`sensor_node_2_tb`', sql_tts_query)
            sql_tts_query = re.sub(r'\bwheat_table\b', '`sensor_node_3_tb`', sql_tts_query)
            sql_tts_query = re.sub(r'\bcorn_table\b', '`sensor_node_4_tb`', sql_tts_query)
            sql_tts_query = re.sub(r'\bFROM WHERE\b', 'FROM', sql_tts_query)
            sql_tts_query = re.sub(r'\bSELECT WHERE\b', 'SELECT', sql_tts_query)

            sql_tts_query_list = list(sql_tts_query.split(" "))

            for i in range(len(sql_tts_query_list)):
                if "apostrophe" in sql_tts_query_list[i]:
                    if sql_tts_query_list[i - 2] != "Date_n_Time" and sql_tts_query_list[i - 3] != "Date_n_Time" and sql_tts_query_list[i - 4] != "Date_n_Time" and sql_tts_query_list[i - 5] != "Date_n_Time":
                        sql_tts_query_list[i - 2] = "Date_n_Time"   
            
            sql_tts_query = ' '.join(sql_tts_query_list)


            if (self.isOptimum):
                sql_tts_query_list = list(sql_tts_query.split(" "))
                chunk = sql_tts_query_list[len(sql_tts_query_list) - sql_tts_query_list[::-1].index('SELECT') : sql_tts_query_list.index('FROM')]
                
                chunk_str = ' '.join(chunk)

                if "WHERE" in sql_tts_query_list:
                    for i in range(len(sql_tts_query_list)):
                        if sql_tts_query_list[i] == 'WHERE':
                            if sql_tts_query_list[i - 1] != "`sensor_node_1_tb`" and sql_tts_query_list[i - 1] != "`sensor_node_2_tb`" and sql_tts_query_list[i - 1] != "`sensor_node_3_tb`" and sql_tts_query_list[i - 1] != "`sensor_node_4_tb`" and sql_tts_query_list[i - 1] != "*" and sql_tts_query_list[i - 1] != "dummy":
                                sql_tts_query_list.insert(i - 3, 'WHERE')
                                break
                    
                    first_where = sql_tts_query_list.index("WHERE")

                    for i in range(len(sql_tts_query_list)):
                        if sql_tts_query_list[i] == 'WHERE' and i != first_where:
                            sql_tts_query_list[i] = 'AND'

                if "WHERE" in sql_tts_query:
                    if "Temperature" in chunk_str:
                        sql_tts_query_list.append(("AND Temperature >= (SELECT opt_temp_from FROM ideal_parameters) AND Temperature <= (SELECT opt_temp_to FROM ideal_parameters)"))
                    elif "Humidity" in chunk_str:
                        sql_tts_query_list.append(("AND Humidity >= (SELECT opt_humid_from FROM ideal_parameters) AND Humidity <= (SELECT opt_humid_to FROM ideal_parameters)"))
                    elif "Light_Intensity" in chunk_str:
                        sql_tts_query_list.append(("AND Light_Intensity >= (SELECT opt_light_from FROM ideal_parameters) AND Light_Intensity <= (SELECT opt_light_to FROM ideal_parameters)"))
                    elif "Soil_Moisture" in chunk_str:
                        sql_tts_query_list.append(("AND Soil_Moisture >= (SELECT opt_soil_from FROM ideal_parameters) AND Soil_Moisture <= (SELECT opt_soil_to FROM ideal_parameters)"))
                    elif "Air_Quality" in chunk_str:
                        sql_tts_query_list.append(("AND Air_Quality >= (SELECT opt_air_from FROM ideal_parameters) AND Air_Quality <= (SELECT opt_air_to FROM ideal_parameters)"))
                else:
                    if "Temperature" in chunk_str:
                        sql_tts_query_list.append(("WHERE Temperature >= (SELECT opt_temp_from FROM ideal_parameters) AND Temperature <= (SELECT opt_temp_to FROM ideal_parameters)"))
                    elif "Humidity" in chunk_str:
                        sql_tts_query_list.append(("WHERE Humidity >= (SELECT opt_humid_from FROM ideal_parameters) AND Humidity <= (SELECT opt_humid_to FROM ideal_parameters)"))
                    elif "Light_Intensity" in chunk_str:
                        sql_tts_query_list.append(("WHERE Light_Intensity >= (SELECT opt_light_from FROM ideal_parameters) AND Light_Intensity <= (SELECT opt_light_to FROM ideal_parameters)"))
                    elif "Soil_Moisture" in chunk_str:
                        sql_tts_query_list.append(("WHERE Soil_Moisture >= (SELECT opt_soil_from FROM ideal_parameters) AND Soil_Moisture <= (SELECT opt_soil_to FROM ideal_parameters)"))
                    elif "Air_Quality" in chunk_str:
                        sql_tts_query_list.append(("WHERE Air_Quality >= (SELECT opt_air_from FROM ideal_parameters) AND Air_Quality <= (SELECT opt_air_to FROM ideal_parameters)"))

                sql_tts_query_str = ' '.join(sql_tts_query_list)             

                return sql_tts_query_str


            return sql_tts_query

        else:
            if temp2 == -1:
                self.err = 'Failed to generate SQL statement parameter unit is invalid'

            elif temp2 == -2:
                self.err = 'Failed to generate SQL statement voice is unrecognizable'

            elif temp2 == -3:
                self.err = 'Sorry I am having some trouble understanding your query please try again'
            
            else:
                self.err = 'Failed to generate SQL statement date is invalid'
            
            return self.err
                













