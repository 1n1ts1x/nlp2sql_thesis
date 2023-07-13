import kivy
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from sql_generator import *
import pyttsx3
import speech_recognition as sr
from preprocessing import *
from sql_generator import *
from text_analysis import *
from replace_substr import *
import threading
from kivy.clock import Clock, mainthread
from functools import partial
from text2digits import text2digits
import re
from dateutil.relativedelta import relativedelta
from sql import *
from queries import *
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.screen import MDScreen
import datetime
from kivy.metrics import dp
from word2number import w2n
from kivy.utils import platform
import datetime

Window.clearcolor = (.9, .9, .9, .9) 

# tts = pyttsx3.init()
# tts.setProperty('rate', 150)

class KVBL(BoxLayout):    
    input_query = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(KVBL, self).__init__(**kwargs)
        self.save_for_later = []
        self.sqlquery = ''
        self.t2d = text2digits.Text2Digits()
        self.isOptimal = False
        self.isGraph = False
        self.isGraphSql = False
        self.isGoodCondition = False
        self.isGoodConditionDate = False
        self.isGoodOrBadConditionDate = False
        self.isAverage = False
        self.tempQuery = ''
        field_value = FieldValue(_key=[], _value=[[], []])
        self.create_data_table(field_value)
    @mainthread 
    def update(self, q, f, *largs):
        if not f:
            if 'SELECT' in q:
                try:
                    self.ids.output_query_txtinput.foreground_color = 0, 1, 0, 1
                    self.ids.output_query_txtinput.text = q
                except:
                    self.ids.output_query_txtinput.text = q
            elif q == '-4':
                q = 'Failed to generate SQL statement date is invalid'
                self.ids.output_query_txtinput.foreground_color = 255, 0, 0, 1
                self.ids.output_query_txtinput.text = 'Failed to generate SQL statement date is invalid'
            elif q == '-5':
                q = 'Sorry I am having some trouble understanding your query please try again'
                self.ids.output_query_txtinput.foreground_color = 255, 0, 0, 1
                self.ids.output_query_txtinput.text = 'Sorry I am having some trouble understanding your query please try again'   
            else:
                self.ids.output_query_txtinput.foreground_color = 255, 0, 0, 1
                self.ids.output_query_txtinput.text = q
        else:
            self.ids.output_query_txtinput.foreground_color = 1, 1, 1, 1
            self.ids.output_query_txtinput.text = q

    def back_to_main(self, q, f):
        self.update(q, f)
            
    def thread_run_tts(self, sql_query='', flag=False):
        if 'SELECT' in sql_query or 'SELECT' in self.tempQuery:
            if flag:
                tts.say(sql_query)
                tts.runAndWait() 
                tts.say('Executing the SQL statement')
                tts.runAndWait()  
                tts.say(self.tempQuery)
                tts.runAndWait()
            else:
                tts.say('Executing the SQL statement')
                tts.runAndWait()    
                tts.say(sql_query)
                tts.runAndWait()
        else:
            if sql_query == '-4':
                sql_query = 'Failed to generate SQL statement date is invalid'
            elif sql_query == '-5':
                sql_query = 'Sorry I am having some trouble understanding your query please try again' 
            tts.say(sql_query)
            tts.runAndWait()
      
    def thread_run_stt(self, query=''):
        r = sr.Recognizer()
        with sr.Microphone() as self.source: 

            Clock.schedule_once(partial(self.update, 'What is your query?', 1), 0)
            tts.say('What is your query?')
            tts.runAndWait()
            tts.stop()

            try:
                audio = r.listen(self.source)
                query = r.recognize_google(audio)    

                Clock.schedule_once(partial(self.update, 'You said', 1), 0)
                tts.say('You said')
                tts.runAndWait()
                Clock.schedule_once(partial(self.update, query, 1), 0)
                tts.say(query)
                tts.runAndWait()
                self.sqlquery = query
            except:                
                tts.say('Failed to generate SQL statement voice is unrecognizable')
                Clock.schedule_once(partial(self.update, 'Failed to generate SQL statement voice is unrecognizable', 0), 0)
                tts.runAndWait()

    def get_x_days(self, input_query_txt, flag, day_str=""):
        today = datetime.datetime.now()
        formatted_date = ""        
        
        if flag:
            words  = input_query_txt.split(" ")
            
            num = [words[idx-1] for idx, word in enumerate(words) if word == "day"]
            
            if '@' in input_query_txt:
                x_days = today - timedelta(days = int(num[0]))
                yesterday = today - timedelta(days = 1)
                formatted_date = "from {} to {}".format(x_days.strftime("%B %d %Y"), yesterday.strftime("%B %d %Y"))
            else:
                x_days = today - timedelta(days = int(num[0]))
                formatted_date = x_days.strftime("on %B %d %Y")
                            
            return input_query_txt.replace("{} day ago".format(num[0]), formatted_date).lower()

        yesterday = today - timedelta(days = 1)
        formatted_date = yesterday.strftime("on %B %d %Y")
        
        return input_query_txt.replace(day_str, formatted_date).lower()

    def get_x_weeks(self, input_query_txt, flag, week_str='', date=''):
        if flag:
            words  = input_query_txt.split(" ")
            
            num = [words[idx-1] for idx, word in enumerate(words) if word == "week"]

            start_date = date + datetime.timedelta(-date.weekday(), weeks=-int(num[0]))

            if '@' in input_query_txt:
                end_date = date + datetime.timedelta(-date.weekday() - 1)
            else:
                end_date = date + datetime.timedelta(-date.weekday() - (1 + (int(num[0]) - 1) * 7))
                
            x_week = "from {} to {}".format(start_date.strftime("%B %d %Y"), end_date.strftime("%B %d %Y"))
                
            return input_query_txt.replace("{} week ago".format(num[0]), x_week).lower()

        start_date = date + datetime.timedelta(-date.weekday(), weeks=-1)
        end_date = date + datetime.timedelta(-date.weekday() - 1)
        x_week = "from {} to {}".format(start_date.strftime("%B %d %Y"), end_date.strftime("%B %d %Y"))
        
        return input_query_txt.replace(week_str, x_week).lower()

    def get_x_months(self, input_query_txt, flag, month_str=''):

        if flag:
            words  = input_query_txt.split(" ")

            num = [words[idx-1] for idx, word in enumerate(words) if word == "month"]

            today = date.today()
            d = today - relativedelta(months=int(num[0]))

            first_day = date(d.year, d.month, 1)
            

            if '@' in input_query_txt:
                last_day = date(today.year, today.month, 1) - relativedelta(days=1)
            else:
                last_day = date(today.year, today.month, 1) - relativedelta(days=1) + relativedelta(months=-(int(num[0]) - 1))
            

            x_month = "from {} to {}".format(first_day.strftime("%B %d %Y"), last_day.strftime("%B %d %Y"))

            return input_query_txt.replace("{} month ago".format(num[0]), x_month).lower()
        
        today = date.today()
        d = today - relativedelta(months=1)

        first_day = date(d.year, d.month, 1)
        

        last_day = date(today.year, today.month, 1) - relativedelta(days=1)
        

        x_month = "from {} to {}".format(first_day.strftime("%B %d %Y"), last_day.strftime("%B %d %Y"))

        return input_query_txt.replace(month_str, x_month).lower()
    

    def get_x_years(self, input_query_txt, flag, year_str=''):

        if flag:
            words  = input_query_txt.split(" ")

            num = [words[idx-1] for idx, word in enumerate(words) if word == "year"]
            
            if '@' in input_query_txt:
                x_year = "from {} to {}".format("january 1 {}".format(int(datetime.date.today().year) - int(num[0])), "december 31 {}".format(int(datetime.date.today().year) - 1))
            else:
                x_year = "from {} to {}".format("january 1 {}".format(int(datetime.date.today().year) - int(num[0])), "december 31 {}".format(int(datetime.date.today().year) - int(num[0])))
            

            return input_query_txt.replace("{} year ago".format(num[0]), x_year).lower()
        

        x_year = "from {} to {}".format("january 1 {}".format(int(datetime.date.today().year) - 1), "december 31 {}".format(int(datetime.date.today().year) - 1))

        return input_query_txt.replace(year_str, x_year).lower()
    
    def convert_string_to_ago_format(self, text):
        patterns = [
            (r'past (\d+) day', r'past \1 day ago @'),
            (r'past (\d+) week', r'past \1 week ago @'),
            (r'past (\d+) month', r'past \1 month ago @'),
            (r'past (\d+) year', r'past \1 year ago @'),
        ]
        for pattern, replacement in patterns:
            text = re.sub(pattern, replacement, text)

        return text

    def replace_worded_numbers(self, input_string):
        words = input_string.split()
        converted_words = []

        for word in words:
            try:
                number = w2n.word_to_num(word)
                converted_words.append(str(number))
            except ValueError:
                converted_words.append(word)

        converted_string = ' '.join(converted_words)
        return converted_string

    def check_and_append_fields(self, query):
            pattern = r"SELECT\s+\*\s+FROM"
            isAsterisk = re.search(pattern, query, re.IGNORECASE)
            if isAsterisk:
                return query
            else:
                select_index = query.index("SELECT")
                from_index = query.index("FROM")

                if self.isGraphSql:
                    queryGraph = re.sub(r"(SELECT)", r"\1 " + "id,", query)
                    return queryGraph
                elif not self.isOptimal:
                    select_pattern = r"SELECT(.+?)FROM"
                    fields = re.search(select_pattern, query, re.IGNORECASE)

                    if fields:
                        fields = fields.group(1).strip()
                        fields_list = [field.strip() for field in fields.split(",")]
                        temp_str = fields_list[0]

                        if "id" not in temp_str:
                            fields_list.insert(0, 'id')

                        if "Date_n_Time" not in temp_str:   
                            fields_list.insert(1, 'Date_n_Time')

                        fields = ", ".join(fields_list)
                        query = re.sub(select_pattern, f'SELECT {fields} FROM', query, flags=re.IGNORECASE)
                        
                        return query

                queryOptimal = query[:select_index + len("SELECT")] + " id, Date_n_Time," + query[select_index + len("SELECT"):from_index] + query[from_index:]

                return queryOptimal
        
        

    def on_enter(self):
        input_query_txt = ' '.join(self.input_query.text.split())
        self.ids.output_query_txtinput.text = ''

        input_query_txt = self.replace_worded_numbers(input_query_txt)

        input_query_txt = input_query_txt.lower()

        input_query_txt = re.sub(r'\btomatoes\b', 'tomato', input_query_txt)
        input_query_txt = re.sub(r'\bgrapes\b', 'grape', input_query_txt)
        input_query_txt = re.sub(r'\bcorns\b', 'corn', input_query_txt)
        input_query_txt = re.sub(r'\bwheats\b', 'wheat', input_query_txt)

        input_query_txt = re.sub(r'\bshow tomato\b', 'show all from tomato', input_query_txt)
        input_query_txt = re.sub(r'\bshow grape\b', 'show all from grape', input_query_txt)
        input_query_txt = re.sub(r'\bshow corn\b', 'show all from corn', input_query_txt)
        input_query_txt = re.sub(r'\bshow wheat\b', 'show all from wheat', input_query_txt)

        input_query_txt = re.sub(r'\bdays\b', 'day', input_query_txt)
        input_query_txt = re.sub(r'\bweeks\b', 'week', input_query_txt)
        input_query_txt = re.sub(r'\bmonths\b', 'month', input_query_txt)
        input_query_txt = re.sub(r'\byears\b', 'year', input_query_txt)
        
        if "condition" in input_query_txt and ("good" in input_query_txt or "optimal" in input_query_txt or "ok" in input_query_txt or "ideal" in input_query_txt or "excellent" in input_query_txt or "best" in input_query_txt or "standard" in input_query_txt):
            self.isGoodCondition = True
        else:
            self.isGoodCondition = False
        
        if ("what is the date" in input_query_txt or "when" in input_query_txt) and "condition" in input_query_txt and ("good" in input_query_txt or "optimal" in input_query_txt or "ok" in input_query_txt or "ideal" in input_query_txt or "excellent" in input_query_txt or "best" in input_query_txt or "standard" in input_query_txt):
            input_query_txt = re.sub(r'\bcore\b', 'optimal', input_query_txt)
            input_query_txt = re.sub(r'\bideal\b', 'optimal', input_query_txt)
            input_query_txt = re.sub(r'\boptimum\b', 'optimal', input_query_txt)
            input_query_txt = re.sub(r'\bbest\b', 'optimal', input_query_txt)
            input_query_txt = re.sub(r'\bbelow optimal\b', 'not within optimal', input_query_txt)
            input_query_txt = re.sub(r'\bbelow the optimal\b', 'not within optimal', input_query_txt)
            input_query_txt = re.sub(r'\bnot optimal\b', 'not within optimal', input_query_txt)
            input_query_txt = re.sub(r'\bnot in optimal\b', 'not within optimal', input_query_txt)
            input_query_txt = re.sub(r'\bbelow optimal\b', 'not within optimal', input_query_txt)
            input_query_txt = re.sub(r'\bin optimal\b', 'within optimal', input_query_txt)
            input_query_txt = re.sub(r'\bwhat is the date\b', 'when', input_query_txt)
            input_query_txt = re.sub(r'\bwhat are the dates\b', 'when', input_query_txt)
            input_query_txt = re.sub(r'\bwhat date\b', 'when', input_query_txt)
            input_query_txt = re.sub(r'\bwhat dates\b', 'within optimal', input_query_txt)

            if "not within optimal" in input_query_txt:
                self.isGoodOrBadConditionDate = True
            elif "within optimal" in input_query_txt:
                self.isGoodOrBadConditionDate = False

            self.isGoodConditionDate = True
        else:
            self.isGoodConditionDate = False

        if "average" in input_query_txt:
            self.isAverage = True
            input_query_txt = re.sub(r'\baverage\b', '', input_query_txt)
        else:
            self.isAverage = False

        input_query_txt = self.convert_string_to_ago_format(input_query_txt)

        if "last day" in input_query_txt:
            input_query_txt = self.get_x_days(input_query_txt, False, "last day")
        elif "previous day" in input_query_txt:
            input_query_txt = self.get_x_days(input_query_txt, False, "previous day")
        elif "past day" in input_query_txt:
            input_query_txt = self.get_x_days(input_query_txt, False, "past day")
        elif "day ago" in input_query_txt:
            input_query_txt = self.get_x_days(input_query_txt, True,)

        if "last week" in input_query_txt:
            input_query_txt = self.get_x_weeks(input_query_txt, False, "last week", datetime.date(int(datetime.date.today().year), int(datetime.date.today().month), int(datetime.date.today().day)))
        elif "previous week" in input_query_txt:
            input_query_txt = self.get_x_weeks(input_query_txt, False, "previous week", datetime.date(int(datetime.date.today().year), int(datetime.date.today().month), int(datetime.date.today().day)))
        elif "past week" in input_query_txt:
            input_query_txt = self.get_x_weeks(input_query_txt, False, "past week", datetime.date(int(datetime.date.today().year), int(datetime.date.today().month), int(datetime.date.today().day)))
        elif "week ago" in input_query_txt:
            input_query_txt = self.get_x_weeks(input_query_txt, True, "", datetime.date(int(datetime.date.today().year), int(datetime.date.today().month), int(datetime.date.today().day)))

        if "last month" in input_query_txt:
            input_query_txt = self.get_x_months(input_query_txt, False, "last month")
        elif "previous month" in input_query_txt:
            input_query_txt = self.get_x_months(input_query_txt, False, "previous month")
        elif "past month" in input_query_txt:
            input_query_txt = self.get_x_months(input_query_txt, False, "past month")
        elif "month ago" in input_query_txt:
            input_query_txt = self.get_x_months(input_query_txt, True)

        if "last year" in input_query_txt:
            input_query_txt = self.get_x_years(input_query_txt, False, "last year")
        elif "previous year" in input_query_txt:
            input_query_txt = self.get_x_years(input_query_txt, False, "previous year")
        elif "past year" in input_query_txt:
            input_query_txt = self.get_x_years(input_query_txt, False, "past year")
        elif "year ago" in input_query_txt:
            input_query_txt = self.get_x_years(input_query_txt, True)
        
        if "graph" in input_query_txt or "plot" in input_query_txt or "trace" in input_query_txt :
            self.isGraph = True
            self.isGraphSql = True
        else:
            self.isGraph = False

        repstr = ReplaceSubstring(input_query_txt)
        input_query_txt = repstr.replace_sub_str()

        if "optimum" in input_query_txt:
            self.isOptimal = True
        else:
            self.isOptimal = False

        print('INPUT: input_query_txt')
        print(input_query_txt)

        prep = CleanText(input_query_txt, self.save_for_later, True)
        t = TextAnalysis(prep.clean_text())

        try:
            t.parse_tokens()
        except:
            # sql_gen = SQLGenerator(prep.clean_text(), tts, prep.lemmatized_tokens2, self.isOptimal, self.isGraph)
            sql_gen = SQLGenerator(prep.clean_text(), prep.lemmatized_tokens2, self.isOptimal, self.isGraph)
            sql_query = sql_gen.generate_sql_statement()

            i = 0

            while i < len(prep.save_for_later) and 'SELECT' not in sql_query and sql_query != '-4' and sql_query != '-5':
                if 'where' == prep.save_for_later[i] and 'is' == prep.save_for_later[i + 1]:
   
                    del prep.save_for_later[i]
                    del prep.save_for_later[i]
                    
                    pi = CleanText(' '.join(prep.save_for_later), prep.save_for_later, False)
                    # sql_geni = SQLGenerator(pi.clean_text(), tts, pi.lemmatized_tokens2)
                    sql_geni = SQLGenerator(pi.clean_text(), pi.lemmatized_tokens2)
                    sql_query = sql_geni.generate_sql_statement()
                
                i += 1
        
        sql_query = re.sub(r'\bHumidity Date_n_Time\b', 'Date_n_Time', sql_query)
        sql_query = re.sub(r'\bTemperature Date_n_Time\b', 'Date_n_Time', sql_query)
        sql_query = re.sub(r'\bSoil_Moisture Date_n_Time\b', 'Date_n_Time', sql_query)
        sql_query = re.sub(r'\bLight_Intensity Date_n_Time\b', 'Date_n_Time', sql_query)
        sql_query = re.sub(r'\bAir_Quality Date_n_Time\b', 'Date_n_Time', sql_query)
        sql_query = re.sub(r'\bDate_n_Time than\b', 'Date_n_Time >=', sql_query)

        sql_query = re.sub(r'\bDate_n_Time equal\b', 'CAST(Date_n_Time AS date) =', sql_query)
        sql_query = re.sub(r'\bDate_n_Time not equal\b', 'CAST(Date_n_Time AS date) !=', sql_query)
        sql_query = re.sub(r'\bDate_n_Time greater than or equal\b', 'CAST(Date_n_Time AS date) >=', sql_query)
        sql_query = re.sub(r'\bDate_n_Time greater than\b', 'CAST(Date_n_Time AS date) >', sql_query)
        sql_query = re.sub(r'\bDate_n_Time less than or equal\b', 'CAST(Date_n_Time AS date) <=', sql_query)
        sql_query = re.sub(r'\bDate_n_Time less than\b', 'CAST(Date_n_Time AS date) <', sql_query)

        sql_query_list = list(sql_query.split(' '))

        try:
            if 'AND' in sql_query_list and 'WHERE' not in sql_query_list:
                sql_query_list[sql_query_list.index('AND')] = 'WHERE'

                sql_query = ' '.join(sql_query_list)
        except:
            None
                
        if self.isAverage:
            chunk = sql_query_list[len(sql_query_list) - sql_query_list[::-1].index('SELECT') : sql_query_list.index('FROM')]
            try:
                del chunk[chunk.index('comma')]
            except:
                pass
            i = 0

            while i < len(sql_query_list):
                j = 0

                while j < len(chunk):
                    if chunk[j] == sql_query_list[i]:
                        sql_query_list[i] = f"AVG({chunk[j]})"

                    j += 1
                i += 1
            
            sql_query = ' '.join(sql_query_list)

        qq = Query()
        print(sql_query_list, "sql_query_list")

        if self.isGoodConditionDate: 
            try:
                where_clause = sql_query_list[sql_query_list.index('WHERE') + 1:]
                table_name = sql_query_list[len(sql_query_list) - sql_query_list[::-1].index('FROM') : sql_query_list.index('WHERE')]

                if self.isGoodOrBadConditionDate:
                    sql_query = qq.prepare_query(' '.join(where_clause), ' '.join(table_name), True, True)
                else:
                    sql_query = qq.prepare_query(' '.join(where_clause), ' '.join(table_name), True, False)
            except:
                table_name = sql_query_list[sql_query_list.index('FROM') + 1:]
                if self.isGoodOrBadConditionDate:
                    sql_query = qq.prepare_query('', ' '.join(table_name), True, True)
                else:
                    sql_query = qq.prepare_query('', ' '.join(table_name), True, False)
        elif self.isGoodCondition: 
            try:
                where_clause = sql_query_list[sql_query_list.index('WHERE') + 1:]
                table_name = sql_query_list[len(sql_query_list) - sql_query_list[::-1].index('FROM') : sql_query_list.index('WHERE')]
                sql_query = qq.prepare_query(' '.join(where_clause), ' '.join(table_name), False)
            except:
                table_name = sql_query_list[sql_query_list.index('FROM') + 1:]
                sql_query = qq.prepare_query('', ' '.join(table_name), False)

        if not self.isGoodConditionDate and not self.isGoodCondition and not self.isGoodOrBadConditionDate:
            sql_query = self.check_and_append_fields(sql_query)

        sql_query_word = sql_query

    

        dict_chars_replace = {'open parenthesis': '(', 'close_parenthesis': ')', ' comma': ',', 'greater than or equal': '>=', 'greater than': '>', 'less than or equal': '<=',
        'less than': '<', 'not equal': '!=', 'equal': '=', 'hyphen': '-', 'apostrophe': "'", 'dummy': '*'}

        try:
            for key, value in dict_chars_replace.items():
                sql_query = sql_query.replace(key, value)
        except:
            pass
        
        print(sql_query, "sql_query")

        if "FROM *" in sql_query:
            from_index = sql_query.index('FROM *')

            before_from = sql_query[:from_index].strip()
            after_asterisk = sql_query[from_index + len('FROM *'):].strip()

            table_names = ['sensor_node_1_tb', 'sensor_node_2_tb', 'sensor_node_3_tb', 'sensor_node_4_tb']

            modified_query = ''
            for table_name in table_names:
                modified_query += before_from + f", '{table_name}' AS src_table FROM `{table_name}` {after_asterisk} UNION "

            sql_query = modified_query.rstrip(' UNION ')


        sql = SQL(self.isGraphSql, self.isGoodCondition, self.isGoodConditionDate, self.isGoodOrBadConditionDate)

        self.isGoodOrBadConditionDate = False

        if self.isGoodCondition or self.isGoodConditionDate: 
            self.tempQuery = sql_query
            sql_query = sql.execute_query(sql_query)
        else:
            sql.execute_query(sql_query)

        self.isGraphSql = False
        
        self.create_data_table(sql.pair)

        if 'SELECT' in sql_query:
            try:
                self.ids.output_query_txtinput.foreground_color = 0, 1, 0, 1
                self.ids.output_query_txtinput.text = sql_query
            except:
                self.ids.output_query_txtinput.text = sql_query
        elif 'SELECT' in self.tempQuery:
            try:
                self.ids.output_query_txtinput.foreground_color = 0, 1, 0, 1
                self.ids.output_query_txtinput.text = sql_query + f"\n{self.tempQuery}"
            except:
                self.ids.output_query_txtinput.text = sql_query
        elif sql_query == '-4':
            sql_query = 'Failed to generate SQL statement date is invalid'
            self.ids.output_query_txtinput.foreground_color = 255, 0, 0, 1
            self.ids.output_query_txtinput.text = 'Failed to generate SQL statement date is invalid'
        elif sql_query == '-5':
            sql_query = 'Sorry I am having some trouble understanding your query please try again'
            self.ids.output_query_txtinput.foreground_color = 255, 0, 0, 1
            self.ids.output_query_txtinput.text = 'Sorry I am having some trouble understanding your query please try again'   
        else:
            self.ids.output_query_txtinput.foreground_color = 255, 0, 0, 1
            self.ids.output_query_txtinput.text = sql_query

        try:
            sql_query_word = sql_query_word.replace('dummy', '*')
        except:
            pass

        # if self.isGoodCondition or self.isGoodConditionDate: 
        #     threading.Thread(target=self.thread_run_tts, args=(sql_query, True,), daemon=True).start()
        # else:
        #     threading.Thread(target=self.thread_run_tts, args=(sql_query, False), daemon=True).start()

    def on_enter2(self):
        self.ids.input_query.text = ''
        self.ids.output_query_txtinput.text = ''

        query = ''
        t = threading.Thread(target=self.thread_run_stt, args=(query,), daemon=True)
        t.start()
        t.join()

        input_query_txt = self.t2d.convert(self.sqlquery)

        repstr = ReplaceSubstring(input_query_txt)
        input_query_txt = repstr.replace_sub_str()

        print('INPUT: input_query_txt')
        print(input_query_txt)
        
        prep = CleanText(input_query_txt, self.save_for_later, True)
        tx = TextAnalysis(prep.clean_text())

        try:
            tx.parse_tokens()
        except:
            sql_gen = SQLGenerator(prep.clean_text(), tts, prep.lemmatized_tokens2)
            sql_query = sql_gen.generate_sql_statement()
 
            sql_geni = ''

            i = 0

            while i < len(prep.save_for_later) and 'SELECT' not in sql_query and sql_query != '-4' and sql_query != '-5':
                if 'where' == prep.save_for_later[i] and 'is' == prep.save_for_later[i + 1]:

                    del prep.save_for_later[i]
                    del prep.save_for_later[i]
                    
                    pi = CleanText(' '.join(prep.save_for_later), prep.save_for_later, False)
                    sql_geni = SQLGenerator(pi.clean_text(), tts, pi.lemmatized_tokens2)
                    sql_query = sql_geni.generate_sql_statement()
                
                i += 1

        sql_query_list = list(sql_query.split(' '))

        try:
            if 'AND' in sql_query_list and 'WHERE' not in sql_query_list:
                sql_query_list[sql_query_list.index('AND')] = 'WHERE'

                sql_query = ' '.join(sql_query_list)
        except:
            None

        sql_query_word = sql_query

        dict_chars_replace = {' comma': ',', 'greater than or equal': '>=', 'greater than': '>', 'less than or equal': '<=',
        'less than': '<', 'not equal': '!=', 'equal': '=', 'hyphen': '-', 'apostrophe': "'", 'dummy': '*'}

        try:
            for key, value in dict_chars_replace.items():
                sql_query = sql_query.replace(key, value)
        except:
            pass

        try:
            Clock.schedule_once(partial(self.update, sql_query, 0), 0)
        finally:
            pass

        try:
            sql_query_word = sql_query_word.replace('dummy', '*')
        except:
            pass

        # threading.Thread(target=self.thread_run_tts, args=(sql_query_word,), daemon=True).start()

    def create_data_table(self, pair=[]):
        data = [[''],['']]
        headers = ['']  

        isData = False

        try:
            if getattr(pair, '_key') and getattr(pair, '_value'):
                data = pair._value
                headers = pair._key
                isData = True
        except:
            pass

        print(pair)


        if len(headers) == 1:
            headers = [headers[0], '']
            for sublist in data:
                sublist.append('')
            

        rows = [[str(value) for value in row] for row in data]  

        table = MDDataTable(
            size_hint =  (1, 0.9),
            column_data = [(header, dp(85)) for header in headers], 
            row_data = rows,
            rows_num = len(data),
            use_pagination = True if isData else False,
            check = False,
        )

        self.ids.data_table_box.clear_widgets()  
        self.ids.data_table_box.add_widget(table)  


class MainApp(MDApp):    
    def build(self):
        # Window.size = (1000, 900) 
        Window.size = (800, 480) 
        self.center_window() 
        return KVBL()

    def center_window(self):
        if platform == 'win':
            self.center_window_windows()
        elif platform == 'linux':
            self.center_window_linux()
        elif platform == 'macosx':
            self.center_window_macos()

    def center_window_windows(self):
        from ctypes import windll

        user32 = windll.user32
        screen_width = user32.GetSystemMetrics(0)
        screen_height = user32.GetSystemMetrics(1)
        window_width, window_height = Window.size

        left = (screen_width - window_width) // 2
        top = (screen_height - window_height) // 2

        Window.left = left
        Window.top = top


    def center_window_linux(self):
        from gi.repository import Gdk

        screen = Gdk.Screen.get_default()
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        window_width, window_height = Window.size

        left = (screen_width - window_width) // 2
        top = (screen_height - window_height) // 2

        Window.position = (left, top)

    def center_window_macos(self):
        from AppKit import NSScreen

        screen_frame = NSScreen.mainScreen().frame()
        screen_width = int(screen_frame.size.width)
        screen_height = int(screen_frame.size.height)
        window_width, window_height = Window.size

        left = (screen_width - window_width) // 2
        top = (screen_height - window_height) // 2

        Window.position = (left, top)

if __name__ == '__main__':
    MainApp().run()
