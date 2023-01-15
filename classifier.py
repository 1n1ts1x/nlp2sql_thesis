import itertools
import re
import speech_recognition as sr

class Classifier:
    def __init__(self, list_toks='', f='', p='', schem='', t='', param_err=0):
        self.list_toks = list_toks
        self.f = f
        self.p = p
        self.schem = schem
        self.t = t
        self.param_err = param_err
        self.save_month = ''
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

    def map_bigram_sql_condition(self, list_toks, p, t, schem_tbl):

        for key in self.month_list:
            i = 0
            
            while i < len(list_toks):
                if key == list_toks[i]:
                    self.save_month = key
                    del list_toks[i]
                    break

                i += 1

        temp = zip(*[list_toks[i:] for i in range(0, 2)])
        list_ngrams = [' '.join(n) for n in temp]

        str = re.sub(r'\d|today', 'x', ' '.join(list_toks))

        str2 = re.sub(r'is|not|above|below|equal', 'y',' '.join(list_toks))

        try:        
            li = list(str.split(' '))

            i = 0

            while i < len(li):
                if li[i] != schem_tbl:
                    li[i] = ''
                else:
                    break
                
                i += 1

            s = ' '.join(li)
        except:
            return -3
        
        if 'temperature' in s and p != 'degree' and p != 0:
            return -1
        if 'humidity' in s and p != 'percent' and p != 0:
            return -1
        if 'soil' in s and p != 'percent' and p != 0:
            return -1
        if 'air' in s and p != 'ppm' and p != 0:
            return -1
        if 'light' in s and p != 'lux' and p != 0:
            return -1
        if 'date' in s and p != 0:
            return -1
        
        check = i = 0

        if p == 'degree':

            if 'x temperature' in str:
                if 'is x' in str:
                    check = 5
                if 'going x' in str:
                    check = 5
                if 'not x' in str:
                    check = 9
                if 'above x' in str:
                    check = 7
                if 'below x' in str:
                    check = 8
                if 'above equal x' in str:
                    check = 1
                if 'not below x' in str:
                    check = 1
                if 'below equal x' in str:
                    check = 2
                if 'not above x' in str:
                    check = 2
                if 'not below equal x' in str:
                    check = 7
                if 'not above equal x' in str:
                    check = 8
            elif 'x humidity' in str:
                return -1
            elif 'x air' in str:
                return -1
            elif 'x light' in str:
                return -1
            elif 'x soil' in str:
                return -1
            elif 'x date' in str:
                return -1
            if 'is x' in str:
                check = 5
            if 'going x' in str:
                check = 5
            if 'not x' in str:
                check = 9
            if 'above x' in str:
                check = 7
            if 'below x' in str:
                check = 8
            if 'above equal x' in str:
                check = 1
            if 'not below x' in str:
                check = 1
            if 'below equal x' in str:
                check = 2
            if 'not above x' in str:
                check = 2
            if 'not below equal x' in str:
                check = 7
            if 'not above equal x' in str:
                check = 8


            if not self.param_err:
                if list_toks.count('humidity') > 1:
                    return -1
                
                if list_toks.count('air') > 1:
                    return -1

                if list_toks.count('light') > 1:
                    return -1
                
                if list_toks.count('soil') > 1:
                    return -1
                
                if list_toks.count('date') > 1:
                    return -1
            else:
                if list_toks.count('humidity') == 1 or list_toks.count('percent') == 1:
                    return -1
                
                if list_toks.count('air') == 1 or list_toks.count('ppm') == 1:
                    return -1

                if list_toks.count('light') == 1 or list_toks.count('lux') == 1:
                    return -1
                
                if list_toks.count('soil') == 1:
                    return -1

                if list_toks.count('date') == 1:
                    return -1
        elif p == 'percent':
            if 'x humidity' in str:
                if 'is x' in str:
                    check = 6
                if 'going x' in str:
                    check = 6
                if 'not x' in str:
                    check = 12
                if 'above x' in str:
                    check = 10
                if 'below x' in str:
                    check = 11
                if 'above equal x' in str:
                    check = 3
                if 'not below x' in str:
                    check = 3
                if 'below equal x' in str:
                    check = 4
                if 'not above x' in str:
                    check = 4
                if 'not below equal x' in str:
                    check = 10
                if 'not above equal x' in str:
                    check = 11
            elif 'humidity is' in str:
                if 'is x' in str:
                    check = 6
                if 'going x' in str:
                    check = 6
                if 'not x' in str:
                    check = 12
                if 'above x' in str:
                    check = 10
                if 'below x' in str:
                    check = 11
                if 'above equal x' in str:
                    check = 3
                if 'not below x' in str:
                    check = 3
                if 'below equal x' in str:
                    check = 4
                if 'not above x' in str:
                    check = 4
                if 'not below equal x' in str:
                    check = 10
                if 'not above equal x' in str:
                    check = 11
            elif 'x soil' in str:
                if 'is x' in str:
                    check = 25
                if 'going x' in str:
                    check = 25
                if 'not x' in str:
                    check = 28
                if 'above x' in str:
                    check = 26
                if 'below x' in str:
                    check = 27
                if 'above equal x' in str:
                    check = 29
                if 'not below x' in str:
                    check = 29
                if 'below equal x' in str:
                    check = 30
                if 'not above x' in str:
                    check = 30
                if 'not below equal x' in str:
                    check = 26
                if 'not above equal x' in str:
                    check = 27
            elif 'soil is' in str:
                if 'is x' in str:
                    check = 25
                if 'going x' in str:
                    check = 25
                if 'not x' in str:
                    check = 28
                if 'above x' in str:
                    check = 26
                if 'below x' in str:
                    check = 27
                if 'above equal x' in str:
                    check = 29
                if 'not below x' in str:
                    check = 29
                if 'below equal x' in str:
                    check = 30
                if 'not above x' in str:
                    check = 30
                if 'not below equal x' in str:
                    check = 26
                if 'not above equal x' in str:
                    check = 27
            elif 'x temperature' in str:
                return -1
            elif 'x air' in str:
                return -1
            elif 'x light' in str:
                return -1
            elif 'x date' in str:
                return -1

            if not self.param_err:
                if list_toks.count('temperature') > 1:
                    return -1
                
                if list_toks.count('air') > 1:
                    return -1

                if list_toks.count('light') > 1:
                    return -1

                if list_toks.count('date') > 1:
                    return -1
            else:
                if list_toks.count('temperature') == 1 or list_toks.count('degrees') == 1:
                    return -1
                
                if list_toks.count('air') == 1 or list_toks.count('ppm') == 1:
                    return -1

                if list_toks.count('light') == 1 or list_toks.count('lux') == 1:
                    return -1

                if list_toks.count('date') == 1:
                    return -1

            if not check:
                humidity_or_soil = 0
                
                t.say('Please choose one between humidity level or soil moisture')
                t.runAndWait()

                r = sr.Recognizer()
                with sr.Microphone() as source: 

                    t.say('Say humidity, to obtain the humidity level or say soil for soil moisture')
                    t.runAndWait()
                    t.stop()

                    audio = r.listen(source)

                    try:
                        humidity_or_soil = r.recognize_google(audio)    

                        t.say('You said')
                        t.runAndWait()
                        t.say(humidity_or_soil)
                        t.runAndWait()
                    except:
                        return -2
                
                i = 0
                
                if humidity_or_soil == 'humidity':
                    if 'is x' in str:
                        check = 6
                    if 'going x' in str:
                        check = 6
                    if 'not x' in str:
                        check = 12
                    if 'above x' in str:
                        check = 10
                    if 'below x' in str:
                        check = 11
                    if 'above equal x' in str:
                        check = 3
                    if 'not below x' in str:
                        check = 3
                    if 'below equal x' in str:
                        check = 4
                    if 'not above x' in str:
                        check = 4
                    if 'not below equal x' in str:
                        check = 10
                    if 'not above equal x' in str:
                        check = 11
                elif humidity_or_soil == 'soil':
                    if 'is x' in str:
                        check = 25
                    if 'going x' in str:
                        check = 25
                    if 'not x' in str:
                        check = 28
                    if 'above x' in str:
                        check = 26
                    if 'below x' in str:
                        check = 27
                    if 'above equal x' in str:
                        check = 29
                    if 'not below x' in str:
                        check = 29
                    if 'below equal x' in str:
                        check = 30
                    if 'not above x' in str:
                        check = 30
                    if 'not below equal x' in str:
                        check = 26
                    if 'not above equal x' in str:
                        check = 27
                else:
                    return -3
        elif p == 'ppm':
            if 'x air' in str:
                if 'is x' in str:
                    check = 13
                if 'going x' in str:
                    check = 13
                if 'not x' in str:
                    check = 16
                if 'above x' in str:
                    check = 14
                if 'below x' in str:
                    check = 15
                if 'above equal x' in str:
                    check = 17
                if 'not below x' in str:
                    check = 17
                if 'below equal x' in str:
                    check = 18
                if 'not above x' in str:
                    check = 18
                if 'not below equal x' in str:
                    check = 14
                if 'not above equal x' in str:
                    check = 15
            elif 'x temperature' in str:
                return -1
            elif 'x humidity' in str:
                return -1
            elif 'x light' in str:
                return -1
            elif 'x soil' in str:
                return -1
            elif 'x date' in str:
                return -1
            if 'is x' in str:
                check = 13
            if 'going x' in str:
                check = 13
            if 'not x' in str:
                check = 16
            if 'above x' in str:
                check = 14
            if 'below x' in str:
                check = 15
            if 'above equal x' in str:
                check = 17
            if 'not below x' in str:
                check = 17
            if 'below equal x' in str:
                check = 18
            if 'not above x' in str:
                check = 18
            if 'not below equal x' in str:
                check = 14
            if 'not above equal x' in str:
                check = 15


            if not self.param_err:
                if list_toks.count('temperature') > 1:
                    return -1
                
                if list_toks.count('humidity') > 1:
                    return -1

                if list_toks.count('light') > 1:
                    return -1

                if list_toks.count('soil') > 1:
                    return -1

                if list_toks.count('date') > 1:
                    return -1
            else:
                if list_toks.count('temperature') == 1 or list_toks.count('degrees') == 1:
                    return -1
                
                if list_toks.count('humidity') == 1 or list_toks.count('percent') == 1:
                    return -1

                if list_toks.count('light') == 1 or list_toks.count('lux') == 1:
                    return -1

                if list_toks.count('soil') == 1:
                    return -1

                if list_toks.count('date') == 1:
                    return -1
        elif p == 'lux':
            if 'x light' in str:
                if 'is x' in str:
                    check = 19
                if 'going x' in str:
                    check = 19
                if 'not x' in str:
                    check = 22
                if 'above x' in str:
                    check = 20
                if 'below x' in str:
                    check = 21
                if 'above equal x' in str:
                    check = 23
                if 'not below x' in str:
                    check = 23
                if 'below equal x' in str:
                    check = 24
                if 'not above x' in str:
                    check = 24
                if 'not below equal x' in str:
                    check = 20
                if 'not above equal x' in str:
                    check = 21
            elif 'x temperature' in str:
                return -1
            elif 'x humidity' in str:
                return -1
            elif 'x air' in str:
                return -1
            elif 'x soil' in str:
                return -1
            elif 'x date' in str:
                return -1
            if 'is x' in str:
                check = 19
            if 'going x' in str:
                check = 19
            if 'not x' in str:
                check = 22
            if 'above x' in str:
                check = 20
            if 'below x' in str:
                check = 21
            if 'above equal x' in str:
                check = 23
            if 'not below x' in str:
                check = 23
            if 'below equal x' in str:
                check = 24
            if 'not above x' in str:
                check = 24
            if 'not below equal x' in str:
                check = 20
            if 'not above equal x' in str:
                check = 21


            if not self.param_err:
                if list_toks.count('temperature') > 1:
                    return -1
                
                if list_toks.count('humidity') > 1:
                    return -1

                if list_toks.count('air') > 1:
                    return -1

                if list_toks.count('soil') > 1:
                    return -1

                if list_toks.count('date') > 1:
                    return -1
            else:
                if list_toks.count('temperature') == 1 or list_toks.count('degrees') == 1:
                    return -1
                
                if list_toks.count('humidity') == 1 or list_toks.count('percent') == 1:
                    return -1

                if list_toks.count('air') == 1 or list_toks.count('ppm') == 1:
                    return -1

                if list_toks.count('soil') == 1:
                    return -1
    
                if list_toks.count('date') == 1:
                    return -1
        else:
            if 'x temperature' in str:
                if 'is x' in str:
                    check = 5
                if 'going x' in str:
                    check = 5
                if 'not x' in str:
                    check = 9
                if 'above x' in str:
                    check = 7
                if 'below x' in str:
                    check = 8
                if 'above equal x' in str:
                    check = 1
                if 'not below x' in str:
                    check = 1
                if 'below equal x' in str:
                    check = 2
                if 'not above x' in str:
                    check = 2
                if 'not below equal x' in str:
                    check = 7
                if 'not above equal x' in str:
                    check = 8
            elif 'temperature y' in str2:
                if 'is x' in str:
                    check = 5
                if 'going x' in str:
                    check = 5
                if 'not x' in str:
                    check = 9
                if 'above x' in str:
                    check = 7
                if 'below x' in str:
                    check = 8
                if 'above equal x' in str:
                    check = 1
                if 'not below x' in str:
                    check = 1
                if 'below equal x' in str:
                    check = 2
                if 'not above x' in str:
                    check = 2
                if 'not below equal x' in str:
                    check = 7
                if 'not above equal x' in str:
                    check = 8      

            if 'x humidity' in str:
                if 'is x' in str:
                    check = 6
                if 'going x' in str:
                    check = 6
                if 'not x' in str:
                    check = 12
                if 'above x' in str:
                    check = 10
                if 'below x' in str:
                    check = 11
                if 'above equal x' in str:
                    check = 3
                if 'not below x' in str:
                    check = 3
                if 'below equal x' in str:
                    check = 4
                if 'not above x' in str:
                    check = 4
                if 'not below equal x' in str:
                    check = 10
                if 'not above equal x' in str:
                    check = 11
            elif 'humidity y' in str2:
                if 'is x' in str:
                    check = 6
                if 'going x' in str:
                    check = 6
                if 'not x' in str:
                    check = 12
                if 'above x' in str:
                    check = 10
                if 'below x' in str:
                    check = 11
                if 'above equal x' in str:
                    check = 3
                if 'not below x' in str:
                    check = 3
                if 'below equal x' in str:
                    check = 4
                if 'not above x' in str:
                    check = 4
                if 'not below equal x' in str:
                    check = 10
                if 'not above equal x' in str:
                    check = 11

            if 'x air' in str:
                if 'is x' in str:
                    check = 13
                if 'going x' in str:
                    check = 13
                if 'not x' in str:
                    check = 16
                if 'above x' in str:
                    check = 14
                if 'below x' in str:
                    check = 15
                if 'above equal x' in str:
                    check = 17
                if 'not below x' in str:
                    check = 17
                if 'below equal x' in str:
                    check = 18
                if 'not above x' in str:
                    check = 18
                if 'not below equal x' in str:
                    check = 14
                if 'not above equal x' in str:
                    check = 15
            elif 'air y' in str2:
                if 'is x' in str:
                    check = 13
                if 'going x' in str:
                    check = 13
                if 'not x' in str:
                    check = 16
                if 'above x' in str:
                    check = 14
                if 'below x' in str:
                    check = 15
                if 'above equal x' in str:
                    check = 17
                if 'not below x' in str:
                    check = 17
                if 'below equal x' in str:
                    check = 18
                if 'not above x' in str:
                    check = 18
                if 'not below equal x' in str:
                    check = 14
                if 'not above equal x' in str:
                    check = 15

            if 'x light' in str:
                if 'is x' in str:
                    check = 19
                if 'going x' in str:
                    check = 19
                if 'not x' in str:
                    check = 22
                if 'above x' in str:
                    check = 20
                if 'below x' in str:
                    check = 21
                if 'above equal x' in str:
                    check = 23
                if 'not below x' in str:
                    check = 23
                if 'below equal x' in str:
                    check = 24
                if 'not above x' in str:
                    check = 24
                if 'not below equal x' in str:
                    check = 20
                if 'not above equal x' in str:
                    check = 21
            elif 'light y' in str2:
                if 'is x' in str:
                    check = 19
                if 'going x' in str:
                    check = 19
                if 'not x' in str:
                    check = 22
                if 'above x' in str:
                    check = 20
                if 'below x' in str:
                    check = 21
                if 'above equal x' in str:
                    check = 23
                if 'not below x' in str:
                    check = 23
                if 'below equal x' in str:
                    check = 24
                if 'not above x' in str:
                    check = 24
                if 'not below equal x' in str:
                    check = 20
                if 'not above equal x' in str:
                    check = 21

            if 'x soil' in str:
                if 'is x' in str:
                    check = 25
                if 'going x' in str:
                    check = 25
                if 'not x' in str:
                    check = 28
                if 'above x' in str:
                    check = 26
                if 'below x' in str:
                    check = 27
                if 'above equal x' in str:
                    check = 29
                if 'not below x' in str:
                    check = 29
                if 'below equal x' in str:
                    check = 30
                if 'not above x' in str:
                    check = 30
                if 'not below equal x' in str:
                    check = 26
                if 'not above equal x' in str:
                    check = 27
            elif 'soil y' in str2:
                if 'is x' in str:
                    check = 25
                if 'going x' in str:
                    check = 25
                if 'not x' in str:
                    check = 28
                if 'above x' in str:
                    check = 26
                if 'below x' in str:
                    check = 27
                if 'above equal x' in str:
                    check = 29
                if 'not below x' in str:
                    check = 29
                if 'below equal x' in str:
                    check = 30
                if 'not above x' in str:
                    check = 30
                if 'not below equal x' in str:
                    check = 26
                if 'not above equal x' in str:
                    check = 27

            if 'x date' in str:
                if 'is x' in str:
                    check = 31
                if 'going x' in str:
                    check = 31
                if 'not x' in str:
                    check = 34
                if 'above x' in str:
                    check = 32
                if 'below x' in str:
                    check = 33
                if 'above equal x' in str:
                    check = 35
                if 'not below x' in str:
                    check = 35
                if 'below equal x' in str:
                    check = 36
                if 'not above x' in str:
                    check = 36
                if 'not below equal x' in str:
                    check = 32
                if 'not above equal x' in str:
                    check = 33
            elif 'date y' in str2:
                if 'is x' in str:
                    check = 31
                if 'going x' in str:
                    check = 31
                if 'not x' in str:
                    check = 34
                if 'above x' in str:
                    check = 32
                if 'below x' in str:
                    check = 33
                if 'above equal x' in str:
                    check = 35
                if 'not below x' in str:
                    check = 35
                if 'below equal x' in str:
                    check = 36
                if 'not above x' in str:
                    check = 36
                if 'not below equal x' in str:
                    check = 32
                if 'not above equal x' in str:
                    check = 33
            elif 'today' in str2:
                str = list(str.split(' '))
                str = ' '.join(list(filter(('today').__ne__, str)))
                str = re.sub(schem_tbl, 'x', str)
   
                if 'is x' in str or 'x is' in str or '' in str:
                    check = 31
                if 'going x' in str or 'x is going' in str:
                    check = 31
                if 'not x' in str or 'x is not' in str or 'is is not' in str or 'not' in str:
                    check = 34
                if 'above x' in str or 'x is above' in str or 'is is above' in str or 'above' in str:
                    check = 32
                if 'below x' in str or 'x is below' in str or 'is is below' in str or 'below' in str:
                    check = 33
                if 'above equal x' in str or 'x is above equal' in str or 'is is above equal' in str or 'above equal' in str:
                    check = 35
                if 'not below x' in str or 'x is not below' in str or 'is is not below' in str or 'not below' in str:
                    check = 35
                if 'below equal x' in str or 'x is below equal' in str or 'is is below equal' in str or 'below equal' in str:
                    check = 36
                if 'not above x' in str or 'x is not above' in str or 'is is not above' in str or 'not above' in str:
                    check = 36
                if 'not below equal x' in str or 'x is not below equal' in str or 'is is not below equal' in str or 'not below equal' in str:
                    check = 32
                if 'not above equal x' in str or 'x is not above equal' in str or 'is is not above equal' in str or 'not above equal' in str:
                    check = 33


        if self.save_month:
            str_tbl_list = list(str.split(' '))
            str = ' '.join(list(filter((schem_tbl).__ne__, str_tbl_list)))

            if 'is x' in str:
                check = 31
            if 'going x' in str:
                check = 31
            if 'not x' in str:
                check = 34
            if 'above x' in str:
                check = 32
            if 'below x' in str:
                check = 33
            if 'above equal x' in str:
                check = 35
            if 'not below x' in str:
                check = 35
            if 'below equal x' in str:
                check = 36
            if 'not above x' in str:
                check = 36
            if 'not below equal x' in str:
                check = 32
            if 'not above equal x' in str:
                check = 33
            list_toks.append(self.save_month)
            
        return check

    def bigram_check(list_toks, schem):
        perm_schem = list(itertools.permutations(schem[0], 2))
        
        temp = zip(*[list_toks[i:] for i in range(0, 2)])
        list_ngrams = [' '.join(n) for n in temp]

        check = i = 0
        
        while i < len(list_ngrams):
            j = 0

            while j < len(perm_schem):
                if list_ngrams[i] == ' '.join(perm_schem[j]):
                    return ', '.join(list_ngrams[i].split())

                j += 1

            if list_ngrams[i] == 'all temperature' or list_ngrams[i] == 'temperature all' or list_ngrams[i] == 'reading temperature':
                check = 1
            if list_ngrams[i] == 'all humidity' or list_ngrams[i] == 'humidity all' or list_ngrams[i] == 'reading humidity':
                check = 2
            if list_ngrams[i] == 'all air' or list_ngrams[i] == 'air all' or list_ngrams[i] == 'reading air':
                check = 3
            if list_ngrams[i] == 'all soil' or list_ngrams[i] == 'soil all' or list_ngrams[i] == 'reading soil':
                check = 4
            if list_ngrams[i] == 'all light' or list_ngrams[i] == 'light all' or list_ngrams[i] == 'reading light':
                check = 5
            if list_ngrams[i] == 'all date' or list_ngrams[i] == 'date all' or list_ngrams[i] == 'reading date':
                check = 5

            i += 1

        if check:
            return check

        return -1

    def trigram_check(list_toks, f, p, schem):
        perm_schem = list(itertools.permutations(schem[0], 3))
        
        temp = zip(*[list_toks[i:] for i in range(0, 3)])
        list_ngrams = [' '.join(n) for n in temp]


        i = 0
        
        while i < len(list_ngrams):
            j = 0

            while j < len(perm_schem):
                if list_ngrams[i] == ' '.join(perm_schem[j]):
                    return ', '.join(list_ngrams[i].split())

                j += 1

            i += 1

        return Classifier.bigram_check(list_toks, schem)

    def fourgram_check(list_toks, f, p, schem):
        perm_schem = list(itertools.permutations(schem[0], 4))
        
        temp = zip(*[list_toks[i:] for i in range(0, 4)])
        list_ngrams = [' '.join(n) for n in temp]

        i = 0
        
        while i < len(list_ngrams):
            j = 0

            while j < len(perm_schem):
                if list_ngrams[i] == ' '.join(perm_schem[j]):
                    return ', '.join(list_ngrams[i].split())

                j += 1

            i += 1
        
        return Classifier.trigram_check(list_toks, f, p, schem)


    def fivegram_check(list_toks, f, p, schem):
        perm_schem = list(itertools.permutations(schem[0], 5))
        
        temp = zip(*[list_toks[i:] for i in range(0, 5)])
        list_ngrams = [' '.join(n) for n in temp]

        i = 0
        
        while i < len(list_ngrams):
            j = 0

            while j < len(perm_schem):
                if list_ngrams[i] == ' '.join(perm_schem[j]):
                    return ', '.join(list_ngrams[i].split())

                j += 1

            i += 1
        
        return Classifier.fourgram_check(list_toks, f, p, schem)

    def sixgram_check(list_toks, f, p, schem):
        perm_schem = list(itertools.permutations(schem[0], 6))
        
        temp = zip(*[list_toks[i:] for i in range(0, 6)])
        list_ngrams = [' '.join(n) for n in temp]

        i = 0
        
        while i < len(list_ngrams):
            j = 0

            while j < len(perm_schem):
                if list_ngrams[i] == ' '.join(perm_schem[j]):
                    return ', '.join(list_ngrams[i].split())

                j += 1

            i += 1
        
        return Classifier.fivegram_check(list_toks, f, p, schem)

    '''n-gram checks'''
    def ngram_check(self):

        if not self.f: 
            list_cols = Classifier.sixgram_check(self.list_toks, self.f, self.p, self.schem)

            if list_cols != -1:
                return list_cols
            
            return 0
        try:
            return self.map_bigram_sql_condition(self.list_toks, self.p, self.t, self.schem[1][0])
        except:
            return -3



























