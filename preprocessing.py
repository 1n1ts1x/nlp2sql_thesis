from certifi import where
import nltk
import re
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import datetime

class CleanText:
    def __init__(self, q='', save_for_later=[], pff=True):
        self.q = q
        self.tokens2 = ''
        self.stopwords2 = ''
        self.lemmatized_tokens2 = ''
        self.params = ['temperature', 'humidity', 'soil', 'light', 'air', 'all', 'date', 'opt_temperature', 'opt_humidity', 'opt_soil', 'opt_light', 'opt_air']
        self.save_for_later = save_for_later
        self.pff = pff
        self.isDateFlag = False
        self.month_ls = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
        self.countMonth = 0

    def arrange_tokens(self, ls, cmd_list):
        month_list = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
        params_list = ['temperature', 'degree', 'humidity', 'soil', 'percent', 'air', 'ppm', 'light', 
        'lux', 'date', 'opt_temperature', 'opt_humidity', 'opt_soil', 'opt_light', 'opt_air']

        try:
            i = 0
            while i < len(ls):
                j = 0
                while j < len(month_list):
                    if ls[i] == month_list[j]:
                        self.countMonth += 1
                        if int(ls[i + 1]) < 32:
                            try:
                                if int(ls[i + 2]) > 1999:
                                    break
                            except:
                                ls.insert(i + 2, "2023")
                        else:
                            break
                    j += 1
                i += 1
        except:
            pass
        

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
            None

            
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

        list_cmd = []
        list_table = []
        list_condition = []
        list_date = []
        list_date2 = []
        ffdate = 0
        ffdate2 = 0
        ffdate3 = 0
        b = 0

        index = index2 = index3 = index4 = index5 = index6 = index7 = index8 = index9 = index10 = 0

        try:
            i = len(ls) - 1
            
            while i >= 0:
                j = i
                if ls[i] == 'table':
                    index3 = i
                    
                    while j >= 0:
                        if ls[j] != 'of':
                            list_table.append(ls[j])
                        else:
                            b = 1
                            break
                        
                        index4 = j - 1
                        j -= 1
                
                if b:
                    break
                
                i -= 1
                
            list_table.reverse()
            
            if 'today' in ls and month:
                i = len(ls) - 1

                while i >= 0:
                    j = i
                
                    if ls[i] == 'today':
                        index5 = i
                        while j >= 0:
                            if ls[j] != 'opt_temperature' and ls[j] != 'opt_humidity' and ls[j] != 'opt_soil' and ls[j] != 'opt_light' and ls[j] != 'opt_air' and ls[j] != 'table' and ls[j] != 'date' and ls[j] != 'degree' and ls[j] != 'percent' and ls[j] != 'lux' and ls[j] != 'ppm' and ls[j] != 'temperature' and ls[j] != 'soil' and ls[j] != 'humidity' and ls[j] != 'air' and ls[j] != 'light' and not ls[j].isnumeric() and ls[j] != 'table' and ls[j] != 'readings' and ls[j] != 'reading' and ls[j] != month and ls[j] != 'all':
                                list_date.append(ls[j])
                            else:
                                break
                            
                            index6 = j
                            j -= 1
                    i -= 1    
            
                list_date.reverse()
                
                i = 0

                while i < len(ls):
                    j = i

                    if ls[i] == cmd:
                        index = i
                        while j < len(ls):
                            if ls[j] != 'of' and ls[j] != 'where' and ls[j] != 'on' and ls[j] != 'today' and ls[j] != 'above' and ls[j] != 'below' and ls[j] != 'not' and 'today' in ls:
                                list_cmd.append(ls[j])
                            else:
                                break
                            
                            index2 = j
                            j += 1
                            
                    elif (ls[i] == 'and' or ls[i] == 'or') and ls[i + 1] == 'is' and ls[i+2] == 'not' and (ls[i + 3] == 'on' or ls[i + 3] == 'above' or ls[i + 3] == 'below') and (ls[i + 4] == month or ls[i + 5] == month or ls[i + 6] == month):
                        index9 = i
                        while j < len(ls):
                            if ls[j] != 'opt_temperature' and ls[j] != 'opt_humidity' and ls[j] != 'opt_soil' and ls[j] != 'opt_light' and ls[j] != 'opt_air' and ls[j] != 'table' and ls[j] != 'degree' and ls[j] != 'percent' and ls[j] != 'lux' and ls[j] != 'ppm' and ls[j] != 'temperature' and ls[j] != 'soil' and ls[j] != 'humidity' and ls[j] != 'air' and ls[j] != 'light' and ls[j] != 'table' and ls[j] != 'where' and ls[j] != cmd and ls[j] != 'today' and ls[j] != 'of':
                                list_date2.append(ls[j])
                                ffdate3 = 1
                                ffdate2 = 1
                                ffdate = 1
                            else:
                                break
                            
                            index10 = j
                            j += 1
                            
                    elif not ffdate3 and (ls[i] == 'and' or ls[i] == 'or') and (ls[i + 1] == 'not' or ls[i + 1] == 'is') and (ls[i + 2] == 'on' or ls[i + 2] == 'above' or ls[i + 2] == 'below') and (ls[i + 3] == month or ls[i + 4] == month or ls[i + 5] == month):
                        index9 = i
                        while j < len(ls):
                            if ls[j] != 'opt_temperature' and ls[j] != 'opt_humidity' and ls[j] != 'opt_soil' and ls[j] != 'opt_light' and ls[j] != 'opt_air' and ls[j] != 'table' and ls[j] != 'degree' and ls[j] != 'percent' and ls[j] != 'lux' and ls[j] != 'ppm' and ls[j] != 'temperature' and ls[j] != 'soil' and ls[j] != 'humidity' and ls[j] != 'air' and ls[j] != 'light'and ls[j] != 'table' and ls[j] != 'where' and ls[j] != cmd and ls[j] != 'today' and ls[j] != 'of':
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
                            if ls[j] != 'opt_temperature' and ls[j] != 'opt_humidity' and ls[j] != 'opt_soil' and ls[j] != 'opt_light' and ls[j] != 'opt_air' and ls[j] != 'table' and ls[j] != 'degree' and ls[j] != 'percent' and ls[j] != 'lux' and ls[j] != 'ppm' and ls[j] != 'temperature' and ls[j] != 'soil' and ls[j] != 'humidity' and ls[j] != 'air' and ls[j] != 'light'and ls[j] != 'table' and ls[j] != 'where' and ls[j] != cmd and ls[j] != 'today' and ls[j] != 'of':
                                list_date2.append(ls[j])
                                ffdate = 1
                            else:
                                break
                            
                            index10 = j
                            j += 1
                            
                    elif not ffdate and (ls[i] == 'on' or ls[i] == 'above' or ls[i] == 'below' or  ls[i] == 'and' or ls[i] == 'or') and (ls[i + 1] == month or ls[i + 2] == month or ls[i + 3] == month):
                        index7 = i
                        while j < len(ls):
                            if ls[j] != 'opt_temperature' and ls[j] != 'opt_humidity' and ls[j] != 'opt_soil' and ls[j] != 'opt_light' and ls[j] != 'opt_air' and ls[j] != 'table' and ls[j] != 'degree' and ls[j] != 'percent' and ls[j] != 'lux' and ls[j] != 'ppm' and ls[j] != 'temperature' and ls[j] != 'soil' and ls[j] != 'humidity' and ls[j] != 'air' and ls[j] != 'light'and ls[j] != 'table' and ls[j] != 'where' and ls[j] != cmd and ls[j] != 'today' and ls[j] != 'of':
                                list_date2.append(ls[j])
                            else:
                                break
                            
                            index8 = j
                            j += 1
                            
                    i += 1

            elif 'today' in ls:
                i = len(ls) - 1
                while i >= 0:
                    j = i
                
                    if ls[i] == 'today':
                        index5 = i
                        while j >= 0:
                            if ls[j] != 'opt_temperature' and ls[j] != 'opt_humidity' and ls[j] != 'opt_soil' and ls[j] != 'opt_light' and ls[j] != 'opt_air' and ls[j] != 'table' and ls[j] != 'date' and ls[j] != 'degree' and ls[j] != 'percent' and ls[j] != 'lux' and ls[j] != 'ppm' and ls[j] != 'temperature' and ls[j] != 'soil' and ls[j] != 'humidity' and ls[j] != 'air' and ls[j] != 'light' and not ls[j].isnumeric() and ls[j] != 'table' and ls[j] != 'readings' and ls[j] != 'reading' and ls[j] != month and ls[j] != 'all':
                                list_date.append(ls[j])
                            else:
                                break
                            index6 = j
                            j -= 1
                    i -= 1    
                    
                list_date.reverse()
                
                i = 0

                while i < len(ls):
                    j = i

                    if ls[i] == cmd:
                        index = i
                        while j < len(ls):
                            if ls[j] != 'of' and ls[j] != 'where' and ls[j] != 'on' and ls[j] != 'today' and ls[j] != 'above' and ls[j] != 'below' and ls[j] != 'not' and 'today' in ls:
                                list_cmd.append(ls[j])
            
                            else:
                                break
                            index2 = j
                            j += 1
                    i += 1

            elif 'yesterday' in ls and month:
                i = len(ls) - 1

                while i >= 0:
                    j = i
                
                    if ls[i] == 'yesterday':
                        index5 = i
                        while j >= 0:
                            if ls[j] != 'opt_temperature' and ls[j] != 'opt_humidity' and ls[j] != 'opt_soil' and ls[j] != 'opt_light' and ls[j] != 'opt_air' and ls[j] != 'table' and ls[j] != 'date' and ls[j] != 'degree' and ls[j] != 'percent' and ls[j] != 'lux' and ls[j] != 'ppm' and ls[j] != 'temperature' and ls[j] != 'soil' and ls[j] != 'humidity' and ls[j] != 'air' and ls[j] != 'light' and not ls[j].isnumeric() and ls[j] != 'table' and ls[j] != 'readings' and ls[j] != 'reading' and ls[j] != month and ls[j] != 'all':
                                list_date.append(ls[j])
                            else:
                                break
                            
                            index6 = j
                            j -= 1
                    i -= 1    
            
                list_date.reverse()
                
                i = 0

                while i < len(ls):
                    j = i

                    if ls[i] == cmd:
                        index = i
                        while j < len(ls):
                            if ls[j] != 'of' and ls[j] != 'where' and ls[j] != 'on' and ls[j] != 'yesterday' and ls[j] != 'above' and ls[j] != 'below' and ls[j] != 'not' and 'yesterday' in ls:
                                list_cmd.append(ls[j])
                            else:
                                break
                            
                            index2 = j
                            j += 1
                            
                    elif (ls[i] == 'and' or ls[i] == 'or') and ls[i + 1] == 'is' and ls[i+2] == 'not' and (ls[i + 3] == 'on' or ls[i + 3] == 'above' or ls[i + 3] == 'below') and (ls[i + 4] == month or ls[i + 5] == month or ls[i + 6] == month):
                        index9 = i
                        while j < len(ls):
                            if ls[j] != 'opt_temperature' and ls[j] != 'opt_humidity' and ls[j] != 'opt_soil' and ls[j] != 'opt_light' and ls[j] != 'opt_air' and ls[j] != 'table' and ls[j] != 'degree' and ls[j] != 'percent' and ls[j] != 'lux' and ls[j] != 'ppm' and ls[j] != 'temperature' and ls[j] != 'soil' and ls[j] != 'humidity' and ls[j] != 'air' and ls[j] != 'light' and ls[j] != 'table' and ls[j] != 'where' and ls[j] != cmd and ls[j] != 'yesterday' and ls[j] != 'of':
                                list_date2.append(ls[j])
                                ffdate3 = 1
                                ffdate2 = 1
                                ffdate = 1
                            else:
                                break
                            
                            index10 = j
                            j += 1
                            
                    elif not ffdate3 and (ls[i] == 'and' or ls[i] == 'or') and (ls[i + 1] == 'not' or ls[i + 1] == 'is') and (ls[i + 2] == 'on' or ls[i + 2] == 'above' or ls[i + 2] == 'below') and (ls[i + 3] == month or ls[i + 4] == month or ls[i + 5] == month):
                        index9 = i
                        while j < len(ls):
                            if ls[j] != 'opt_temperature' and ls[j] != 'opt_humidity' and ls[j] != 'opt_soil' and ls[j] != 'opt_light' and ls[j] != 'opt_air' and ls[j] != 'table' and ls[j] != 'degree' and ls[j] != 'percent' and ls[j] != 'lux' and ls[j] != 'ppm' and ls[j] != 'temperature' and ls[j] != 'soil' and ls[j] != 'humidity' and ls[j] != 'air' and ls[j] != 'light'and ls[j] != 'table' and ls[j] != 'where' and ls[j] != cmd and ls[j] != 'yesterday' and ls[j] != 'of':
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
                            if ls[j] != 'opt_temperature' and ls[j] != 'opt_humidity' and ls[j] != 'opt_soil' and ls[j] != 'opt_light' and ls[j] != 'opt_air' and ls[j] != 'table' and ls[j] != 'degree' and ls[j] != 'percent' and ls[j] != 'lux' and ls[j] != 'ppm' and ls[j] != 'temperature' and ls[j] != 'soil' and ls[j] != 'humidity' and ls[j] != 'air' and ls[j] != 'light'and ls[j] != 'table' and ls[j] != 'where' and ls[j] != cmd and ls[j] != 'yesterday' and ls[j] != 'of':
                                list_date2.append(ls[j])
                                ffdate = 1
                            else:
                                break
                            
                            index10 = j
                            j += 1
                            
                    elif not ffdate and (ls[i] == 'on' or ls[i] == 'above' or ls[i] == 'below' or  ls[i] == 'and' or ls[i] == 'or') and (ls[i + 1] == month or ls[i + 2] == month or ls[i + 3] == month):
                        index7 = i
                        while j < len(ls):
                            if ls[j] != 'opt_temperature' and ls[j] != 'opt_humidity' and ls[j] != 'opt_soil' and ls[j] != 'opt_light' and ls[j] != 'opt_air' and ls[j] != 'table' and ls[j] != 'degree' and ls[j] != 'percent' and ls[j] != 'lux' and ls[j] != 'ppm' and ls[j] != 'temperature' and ls[j] != 'soil' and ls[j] != 'humidity' and ls[j] != 'air' and ls[j] != 'light'and ls[j] != 'table' and ls[j] != 'where' and ls[j] != cmd and ls[j] != 'yesterday' and ls[j] != 'of':
                                list_date2.append(ls[j])
                            else:
                                break
                            
                            index8 = j
                            j += 1
                            
                    i += 1

            elif 'yesterday' in ls:
                i = len(ls) - 1
                while i >= 0:
                    j = i
                
                    if ls[i] == 'yesterday':
                        index5 = i
                        while j >= 0:
                            if ls[j] != 'opt_temperature' and ls[j] != 'opt_humidity' and ls[j] != 'opt_soil' and ls[j] != 'opt_light' and ls[j] != 'opt_air' and ls[j] != 'table' and ls[j] != 'date' and ls[j] != 'degree' and ls[j] != 'percent' and ls[j] != 'lux' and ls[j] != 'ppm' and ls[j] != 'temperature' and ls[j] != 'soil' and ls[j] != 'humidity' and ls[j] != 'air' and ls[j] != 'light' and not ls[j].isnumeric() and ls[j] != 'table' and ls[j] != 'readings' and ls[j] != 'reading' and ls[j] != month and ls[j] != 'all':
                                list_date.append(ls[j])
                            else:
                                break
                            index6 = j
                            j -= 1
                    i -= 1    
                    
                list_date.reverse()
                
                i = 0

                while i < len(ls):
                    j = i

                    if ls[i] == cmd:
                        index = i
                        while j < len(ls):
                            if ls[j] != 'of' and ls[j] != 'where' and ls[j] != 'on' and ls[j] != 'yesterday' and ls[j] != 'above' and ls[j] != 'below' and ls[j] != 'not' and 'yesterday' in ls:
                                list_cmd.append(ls[j])
            
                            else:
                                break
                            index2 = j
                            j += 1
                    i += 1

            elif month:
                i = 0
                self.isDateFlag = True
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

                    elif (ls[i] == 'and' or ls[i] == 'or') and ls[i + 1] == 'is' and ls[i + 2] == 'not' and (ls[i + 3] == 'on' or ls[i + 3] == 'above' or ls[i + 3] == 'below') and (ls[i + 4] == month or ls[i + 5] == month or ls[i + 6] == month):
                        index9 = i
                        while j < len(ls):
                            if ls[j] != 'opt_temperature' and ls[j] != 'opt_humidity' and ls[j] != 'opt_soil' and ls[j] != 'opt_light' and ls[j] != 'opt_air' and ls[j] != 'table' and ls[j] != 'degree' and ls[j] != 'percent' and ls[j] != 'lux' and ls[j] != 'ppm' and ls[j] != 'temperature' and ls[j] != 'soil' and ls[j] != 'humidity' and ls[j] != 'air' and ls[j] != 'light'and ls[j] != 'table' and ls[j] != 'where' and ls[j] != cmd and ls[j] != 'of':
                                list_date2.append(ls[j])
                                ffdate3 = 1
                                ffdate2 = 1
                                ffdate = 1
                            else:
                                break
                            
                            index10 = j
                            j += 1
                            
                    elif not ffdate3 and (ls[i] == 'and' or ls[i] == 'or') and (ls[i + 1] == 'not' or ls[i + 1] == 'is') and (ls[i + 2] == 'on' or ls[i + 2] == 'above' or ls[i + 2] == 'below') and (ls[i + 3] == month or ls[i + 4] == month or ls[i + 5] == month):
                        index9 = i
                        while j < len(ls):
                            if ls[j] != 'opt_temperature' and ls[j] != 'opt_humidity' and ls[j] != 'opt_soil' and ls[j] != 'opt_light' and ls[j] != 'opt_air' and ls[j] != 'table' and ls[j] != 'degree' and ls[j] != 'percent' and ls[j] != 'lux' and ls[j] != 'ppm' and ls[j] != 'temperature' and ls[j] != 'soil' and ls[j] != 'humidity' and ls[j] != 'air' and ls[j] != 'light'and ls[j] != 'table' and ls[j] != 'where' and ls[j] != cmd and ls[j] != 'of':
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
                            if ls[j] != 'opt_temperature' and ls[j] != 'opt_humidity' and ls[j] != 'opt_soil' and ls[j] != 'opt_light' and ls[j] != 'opt_air' and ls[j] != 'table' and ls[j] != 'degree' and ls[j] != 'percent' and ls[j] != 'lux' and ls[j] != 'ppm' and ls[j] != 'temperature' and ls[j] != 'soil' and ls[j] != 'humidity' and ls[j] != 'air' and ls[j] != 'light'and ls[j] != 'table' and ls[j] != 'where' and ls[j] != cmd and ls[j] != 'of':
                                list_date2.append(ls[j])
                                ffdate = 1
                            else:
                                break
                            
                            index10 = j
                            j += 1
                            
                    elif not ffdate and (ls[i] == 'on' or ls[i] == 'above' or ls[i] == 'below' or  ls[i] == 'and' or ls[i] == 'or') and (ls[i + 1] == month or ls[i + 2] == month or ls[i + 3] == month):
                        index7 = i
                        while j < len(ls):
                            if ls[j] != 'opt_temperature' and ls[j] != 'opt_humidity' and ls[j] != 'opt_soil' and ls[j] != 'opt_light' and ls[j] != 'opt_air' and ls[j] != 'table' and ls[j] != 'degree' and ls[j] != 'percent' and ls[j] != 'lux' and ls[j] != 'ppm' and ls[j] != 'temperature' and ls[j] != 'soil' and ls[j] != 'humidity' and ls[j] != 'air' and ls[j] != 'light'and ls[j] != 'table' and ls[j] != 'where' and ls[j] != cmd and ls[j] != 'of':
                                list_date2.append(ls[j])
                            else:
                                break
                            
                            index8 = j
                            j += 1
                            
                    i += 1
            else:
                i = 0

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
                            
                    i += 1
        except:
            None

        r = []
        r2 = []
        r3 = []
        r4 = []
        r5 = []

        i = len(list_cmd) - 1

        while i >= 0:
            if (list_cmd[i] != 'opt_temperature' and list_cmd[i] != 'opt_humidity' and list_cmd[i] != 'opt_soil' and list_cmd[i] != 'opt_light' and list_cmd[i] != 'opt_air' and list_cmd[i] != 'temperature' and list_cmd[i] != 'humidity' and list_cmd[i] != 'soil' and list_cmd[i] != 'light' and list_cmd[i] != 'air' and list_cmd[i] != 'date' and list_cmd[i] != 'all'):
                list_cmd[i] = ''
            else:
                break
            
            i -= 1
            
        list_cmd = [x for x in list_cmd if x != '']

        seen = set()
        seen_add = seen.add
        list_cmd = [x for x in list_cmd if not (x in seen or seen_add(x))]

        check_tbl = 0

        if not len(list_table):
            check_tbl = 1

        i = len(list_table) - 1

        while i >= 0:
            if list_table[i] != 'table' and list_table[i] != 'plant':
                list_table[i] = ''
            else:
                break
            
            i -= 1
        try:    
            list_table = [x for x in list_table if x != '']
        except:
            pass

        try:    
            list_table = [x for x in list_table if x != 'and']
        except:
            pass

        try:    
            list_table = [x for x in list_table if x != 'or']
        except:
            pass

        try:    
            list_table = [x for x in list_table if x != 'the']
        except:
            pass

        try:    
            list_table = [x for x in list_table if x != 'of']
        except:
            pass

        try:    
            list_table = [x for x in list_table if x != 'table']
        except:
            pass

            
        seen = set()
        seen_add = seen.add
        list_table = [x for x in list_table if not (x in seen or seen_add(x))]

        if 'all' in list_table:
            try:    
                list_table = [x for x in list_table if x == 'all']
            except:
                pass
            
        str_table = ' table '.join(list_table)

        list_table = list(str_table.split(' '))
        list_table.insert(0, 'of')
        list_table.insert(1, 'the')
        list_table.append('table')

        i = len(list_date2) - 1

        while i >= 0:
            if not list_date2[i].isnumeric() and list_date2[i] != month:
                list_date2[i] = ''
            else:
                break
            
            i -= 1
    
        list_date2 = [x for x in list_date2 if x != '']

        try:
            for x in range(index, index2 + 1):
                r.append(x)
            for x in range(index4, index3 + 1):
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

        check = any(i in list_condition for i in params_list)

        if check:
            if 'where' not in list_condition:
                list_condition.insert(0, 'where')
        else:
            list_condition = []

        i = len(list_condition) - 1

        while i >= 0:
            if (list_condition[i] != 'opt_temperature' and list_condition[i] != 'opt_humidity' and list_condition[i] != 'opt_soil' and list_condition[i] != 'opt_light' and list_condition[i] != 'opt_air' and list_condition[i] != 'temperature' and list_condition[i] != 'humidity' and list_condition[i] != 'soil' and list_condition[i] != 'light' and list_condition[i] != 'air' and list_condition[i] != 'date' and list_condition[i] != 'degree' and list_condition[i] != 'percent' and list_condition[i] != 'ppm' and list_condition[i] != 'lux' and not list_condition[i].isnumeric()):
                list_condition[i] = ''
            else:
                break
            
            i -= 1

        try:    
            list_condition = [x for x in list_condition if x != '']
            
            if list_condition[0] == 'and' or list_condition[0] == 'or':
                del list_condition[0]
        except:
            None

        try:
            list_cmd = [x for x in list_cmd if x != 'and']
        except:
            None
            
        try:
            list_cmd = [x for x in list_cmd if x != 'or']
        except:
            None

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

        if 'yesterday' in ls:
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
        
            seen = set()
            seen_add = seen.add
            list_date2 = [x for x in list_date2 if not (x in seen or seen_add(x))]

            if 'or' in list_date2:
                list_date2 = [x for x in list_date2 if x != 'and']
        
            tokens.extend(list_date2)


        if tokens[tokens.index('table') - 1] == '' or tokens[tokens.index('table') - 1] == 'all':
            tokens[tokens.index('table') - 1] = 'dummy'

        if not list_condition and not list_date and not list_date2 and check_tbl:

            i = len(list_cmd) - 1

            while i >= 0:
                if (list_cmd[i] != 'opt_temperature' and list_cmd[i] != 'opt_humidity' and list_cmd[i] != 'opt_soil' and list_cmd[i] != 'opt_light' and list_cmd[i] != 'opt_air' and list_cmd[i] != 'temperature' and list_cmd[i] != 'humidity' and list_cmd[i] != 'soil' and list_cmd[i] != 'light' and list_cmd[i] != 'air' and list_cmd[i] != 'date' and list_cmd[i] != 'all'):
                    list_cmd[i] = ''
                else:
                    break
                
                i -= 1

            if 'all' in list_cmd:
                check2 = any(i in list_cmd for i in params_list)

                if check2:
                    try:
                        list_cmd = [x for x in list_cmd if x != 'all']
                    except:
                        None

            tokens = list_cmd.copy()

        if tokens:
            return tokens
        
        return ls

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

    # def insert_optimum_params(self, tokens, start_str, end_idx, flag):
    #     params_list = ['temperature', 'degree', 'humidity', 'soil', 'percent', 'air', 'ppm', 'light', 'lux', 'date']

    #     start = tokens.index(start_str) if start_str in tokens else None
    #     end = end_idx

    #     if not flag:
    #         end = tokens.index(end)
    #     else:
    #         end -= 1

        
    #     if start is not None:

    #         while start < end:
    #             i = 0
    #             while i < len(params_list):
    #                 if tokens[end] == params_list[i]:
    #                     tokens[end] = "opt_" + tokens[end]
    #                     end -= 1
    #                 i += 1
                    
    #             end -= 1

    #         i = 0

    #         while i < len(params_list):
    #             if tokens[start + 1] == params_list[i]:
    #                 tokens[start + 1] = "opt_" + tokens[start + 1]
    #                 break
    #             i += 1
                
    #         del tokens[start]

    #     return tokens

    '''transform input query to cleaner text'''
    def clean_text(self):
        cmd_list = ['show', 'display', 'list', 'get', 'what']

        #convert query to lowercase
        lowercase_query = self.q.lower()

        #remove punctuation marks and tokenize
        tokenizer = nltk.RegexpTokenizer(r'\w+')
        tokens = tokenizer.tokenize(lowercase_query)

        print('BEFORE: tokens = self.arrange_tokens(tokens, cmd_list)')    
        print(tokens)

        saved_date = []

        try:
            for i in range(len(tokens)):
                if tokens[i] == 'date' and tokens[i + 1] == 'is' and tokens[i + 2] == 'not' and tokens[i + 3] == 'above':
                    saved_date.append(tokens[i + 4])
                    saved_date.append(tokens[i + 5])
                    saved_date.append(tokens[i + 6])
        except:
            pass

        tokens = self.arrange_tokens(tokens, cmd_list)
        print('AFTER: tokens = self.arrange_tokens(tokens, cmd_list)')    
        print(tokens)
        
        try:
            start_before_where_tokens = tokens[:tokens.index('where')]

            where_to_end_tokens = tokens[tokens.index('where'):]

            params = ['temperature', 'humidity', 'air', 'soil', 'light', 'degree', 'percent', 'ppm', 'lux', 'opt_temperature', 'opt_humidity', 'opt_soil', 'opt_light', 'opt_air']

            pcheck = i = 0

            while i < len(where_to_end_tokens):
                j = 0
                
                while j < len(params):
                    if where_to_end_tokens[i] == params[j]:
                        pcheck = params[j]
                        break
                    
                    j += 1
                
                if (where_to_end_tokens[i] == 'and' or where_to_end_tokens[i] == 'or') and where_to_end_tokens[i + 1] == 'not' and where_to_end_tokens[i + 2] == 'between' and (where_to_end_tokens[i + 4] == 'and' or where_to_end_tokens[i + 4] == 'or'):
                    if int(where_to_end_tokens[i + 3]) > int(where_to_end_tokens[i + 5]):
                        temp = where_to_end_tokens[i + 3]
                        where_to_end_tokens[i + 3] = where_to_end_tokens[i + 5]
                        where_to_end_tokens[i + 5] = temp
                        
                        pcheck = pcheck + ' is not below equal'
                        where_to_end_tokens[i + 2] = 'above equal'
                        where_to_end_tokens.insert(i + 5, pcheck)
                        
                        i += 1
                    else:
                        pcheck = pcheck + ' is not below equal'
                        where_to_end_tokens[i + 2] = 'above equal'
                        where_to_end_tokens.insert(i + 5, pcheck)

                        i += 1
                elif (where_to_end_tokens[i] == 'and' or where_to_end_tokens[i] == 'or') and where_to_end_tokens[i + 1] == 'between' and (where_to_end_tokens[i + 3] == 'and' or where_to_end_tokens[i + 3] == 'or'):
                    if int(where_to_end_tokens[i + 2]) > int(where_to_end_tokens[i + 4]):
                        temp = where_to_end_tokens[i + 2]
                        where_to_end_tokens[i + 2] = where_to_end_tokens[i + 4]
                        where_to_end_tokens[i + 4] = temp
                        
                        pcheck = pcheck + ' is below equal'
                        where_to_end_tokens[i + 1] = 'above equal'
                        where_to_end_tokens.insert(i + 4, pcheck)
                        
                        i += 1
                    else:
                        pcheck = pcheck + ' is below equal'
                        where_to_end_tokens[i + 1] = 'above equal'
                        where_to_end_tokens.insert(i + 4, pcheck)

                        i += 1
                        
                i += 1

            pcheck = i = 0

            while i < len(where_to_end_tokens):
                j = 0
                
                while j < len(params):
                    if where_to_end_tokens[i] == params[j]:
                        pcheck = params[j]
                        break
                    
                    j += 1
                
                if where_to_end_tokens[i] == 'not' and where_to_end_tokens[i + 1] == 'between' and (where_to_end_tokens[i + 3] == 'and' or where_to_end_tokens[i + 3] == 'or'):
                    if int(where_to_end_tokens[i + 2]) > int(where_to_end_tokens[i + 4]):
                        temp = where_to_end_tokens[i + 2]
                        where_to_end_tokens[i + 2] = where_to_end_tokens[i + 4]
                        where_to_end_tokens[i + 4] = temp
                        
                        pcheck = pcheck + ' is not below equal'
                        where_to_end_tokens[i + 1] = 'above equal'
                        where_to_end_tokens.insert(i + 4, pcheck)
                        
                        i += 1
                    else:
                        pcheck = pcheck + ' is not below equal'
                        where_to_end_tokens[i + 1] = 'above equal'
                        where_to_end_tokens.insert(i + 4, pcheck)
                        
                        i += 1
                elif where_to_end_tokens[i] == 'is' and where_to_end_tokens[i + 1] == 'between' and (where_to_end_tokens[i + 3] == 'and' or where_to_end_tokens[i + 3] == 'or'):
                    if int(where_to_end_tokens[i + 2]) > int(where_to_end_tokens[i + 4]):
                        temp = where_to_end_tokens[i + 2]
                        where_to_end_tokens[i + 2] = where_to_end_tokens[i + 4]
                        where_to_end_tokens[i + 4] = temp
                        
                        pcheck = pcheck + ' is below equal'
                        where_to_end_tokens[i + 1] = 'above equal'
                        where_to_end_tokens.insert(i + 4, pcheck)
                        
                        i += 1
                    else:
                        pcheck = pcheck + ' is below equal'
                        where_to_end_tokens[i + 1] = 'above equal'
                        where_to_end_tokens.insert(i + 4, pcheck)
                        
                        i += 1
                        
                i += 1

            where_to_end_tokens = list(' '.join(where_to_end_tokens).split(' '))

            params = ['temperature', 'humidity', 'air', 'soil', 'light', 'opt_temperature', 'opt_humidity', 'opt_soil', 'opt_light', 'opt_air']
            params2 = ['degree', 'percent', 'ppm', 'lux']
                
            pcheck = dont_pcheck = 0

            i = len(where_to_end_tokens) - 3

            while i >= 0:
                if (where_to_end_tokens[i] == 'and' or where_to_end_tokens[i] == 'or') and where_to_end_tokens[i + 2] == 'of' and where_to_end_tokens[i + 3] == 'the' and (where_to_end_tokens[i + 4] == 'opt_temperature' or where_to_end_tokens[i + 4] == 'opt_humidity' or where_to_end_tokens[i + 4] == 'opt_soil' or where_to_end_tokens[i + 4] == 'opt_light' or where_to_end_tokens[i + 4] == 'opt_air' or where_to_end_tokens[i + 4] == 'temperature' or where_to_end_tokens[i + 4] == 'humidity' or where_to_end_tokens[i + 4] == 'soil' or where_to_end_tokens[i + 4] == 'light' or where_to_end_tokens[i + 4] == 'air'):
                    where_to_end_tokens.insert(i + 1, where_to_end_tokens[i + 4])
                    i += 1
                elif (where_to_end_tokens[i] == 'and' or where_to_end_tokens[i] == 'or') and where_to_end_tokens[i + 2] == 'of' and (where_to_end_tokens[i + 3] == 'opt_temperature' or where_to_end_tokens[i + 3] == 'opt_humidity' or where_to_end_tokens[i + 3] == 'opt_soil' or where_to_end_tokens[i + 3] == 'opt_light' or where_to_end_tokens[i + 3] == 'opt_air' or where_to_end_tokens[i + 3] == 'temperature' or where_to_end_tokens[i + 3] == 'humidity' or where_to_end_tokens[i + 3] == 'soil' or where_to_end_tokens[i + 3] == 'light' or where_to_end_tokens[i + 3] == 'air'):
                    where_to_end_tokens.insert(i + 1, where_to_end_tokens[i + 3])
                    i += 1
                                        
                i -= 1

            i = len(where_to_end_tokens) - 1

            while i >= 0:
                if where_to_end_tokens[i] != 'and' and where_to_end_tokens[i] != 'or':
                    j = 0
                    
                    
                    while j < len(params2):
                        if where_to_end_tokens[i] == params2[j]:
                            dont_pcheck = 1
                            break
                        
                        j += 1
                        
                    j = 0
                    
                    while j < len(params):
                        if where_to_end_tokens[i] == params[j]:
                            pcheck = 1
                            break
                        
                        j += 1
                else:
                    if dont_pcheck:
                        where_to_end_tokens.insert(i + 1, 'is')
                    elif not pcheck:
                        pindex = i - 1
                        flag = 0

                        while pindex >= 0:
                            pz = 0
                            
                            while pz < len(params):
                                if where_to_end_tokens[pindex] == params[pz]:
                                    flag = 1
                                    where_to_end_tokens.insert(i + 1, params[pz])
                                    break
                                
                                pz += 1
                            
                            if flag:
                                break

                            pindex -= 1
                    
                    pcheck = dont_pcheck = 0
                                        
                i -= 1


            start_before_where_tokens.extend(where_to_end_tokens)
            tokens = start_before_where_tokens
        except:
            pass

        flag = 0

        if 'table' in tokens or 'plant' in tokens:
            flag = 1

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
            try:
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
            except:
                pass

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

        if (not self.isDateFlag):
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
        
        if (self.countMonth > 1): 
            try: 
                i = len(self.tokens2) - 1

                while i >= 0:
                    j = 0

                    while j < len(self.month_ls):
                        if self.tokens2[i] == self.month_ls[j]:
                            if self.tokens2[i - 1].isnumeric():
                                self.tokens2.insert(i, "and")
                                self.tokens2.insert(i + 1, "date")
                                self.tokens2.insert(i + 2, "is")
                        j += 1
                    i -= 1
            except: 
                pass

            try: 
                i = len(self.tokens2) - 1

                while i >= 0:
                    if self.tokens2[i] == "above" and int(self.tokens2[i - 1]) > 1999:
                        self.tokens2.insert(i, "and")
                        self.tokens2.insert(i + 1, "date")
                        self.tokens2.insert(i + 2, "is")
                        self.tokens2.insert(i + 3, "not")
                        break
                    i -= 1
            except: 
                pass

        print(self.tokens2, self.countMonth,self.countMonth,self.countMonth,self.countMonth, "PRE-PROCESS BEFORE LEMMA")
        
        try:
            if (len(saved_date) < 3):
                saved_date.append(str(datetime.date.today().year))

            for i in range(len(self.tokens2)):
                if self.tokens2[i] == 'date' and self.tokens2[i + 1] == 'is' and self.tokens2[i + 2] == 'not' and self.tokens2[i + 3] == 'above':
                    if self.tokens2[i + 4].isnumeric():
                        del self.tokens2[i + 4]
                        self.tokens2.append(saved_date[0]) 
                        self.tokens2.append(saved_date[1]) 
                        self.tokens2.append(saved_date[2]) 
        except:
            pass
        
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
        custom_stopwords.append('intensity')
        custom_stopwords.append('moisture')
        custom_stopwords.append('equivalent')
        custom_stopwords.append('exactly')
        stopword_tokens = [word for word in tokens if word not in custom_stopwords]

        #lemmatize
        wordnet_lemmatizer = WordNetLemmatizer()
        lemmatized_tokens = [wordnet_lemmatizer.lemmatize(word) for word in stopword_tokens]
        
        try:
            if lemmatized_tokens:
                if lemmatized_tokens[0] == temp:
                    lemmatized_tokens[0] = ''
                    lemmatized_tokens[1] = ''
        except:
            None
            
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
        custom_stopwords.append('intensity')
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

        print("lemmatized tokens")
        print(lemmatized_tokens)

        return lemmatized_tokens
















