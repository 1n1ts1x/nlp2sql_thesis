import kivy
from kivy.app import App
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

Window.clearcolor = (.9, .9, .9, .9) 

tts = pyttsx3.init()
tts.setProperty('rate', 150)

class KVBL(BoxLayout):    
    input_query = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(KVBL, self).__init__(**kwargs)
        self.save_for_later = []
        self.sqlquery = ''
        self.t2d = text2digits.Text2Digits()
        self.isOptimal = False
        self.isGraph = False

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
            
    def thread_run_tts(self, sql_query=''):
        if 'SELECT' in sql_query:
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
                

    def on_enter(self):
        input_query_txt = ' '.join(self.input_query.text.split())
        self.ids.output_query_txtinput.text = ''

        input_query_txt = input_query_txt.lower()

        if "graph" in input_query_txt or "plot" in input_query_txt or "trace" in input_query_txt :
            self.isGraph = True
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
            sql_gen = SQLGenerator(prep.clean_text(), tts, prep.lemmatized_tokens2, self.isOptimal, self.isGraph)
            sql_query = sql_gen.generate_sql_statement()

            i = 0

            while i < len(prep.save_for_later) and 'SELECT' not in sql_query and sql_query != '-4' and sql_query != '-5':
                if 'where' == prep.save_for_later[i] and 'is' == prep.save_for_later[i + 1]:
   
                    del prep.save_for_later[i]
                    del prep.save_for_later[i]
                    
                    pi = CleanText(' '.join(prep.save_for_later), prep.save_for_later, False)
                    sql_geni = SQLGenerator(pi.clean_text(), tts, pi.lemmatized_tokens2)
                    sql_query = sql_geni.generate_sql_statement()
                
                i += 1
        
        sql_query = re.sub(r'\bHumidity Date_n_Time\b', 'Date_n_Time', sql_query)
        sql_query = re.sub(r'\bTemperature Date_n_Time\b', 'Date_n_Time', sql_query)
        sql_query = re.sub(r'\bSoil_Moisture Date_n_Time\b', 'Date_n_Time', sql_query)
        sql_query = re.sub(r'\bLight_Intensity Date_n_Time\b', 'Date_n_Time', sql_query)
        sql_query = re.sub(r'\bAir_Quality Date_n_Time\b', 'Date_n_Time', sql_query)
        sql_query = re.sub(r'\bDate_n_Time than\b', 'Date_n_Time >=', sql_query)

        sql_query_list = list(sql_query.split(' '))

        try:
            if 'AND' in sql_query_list and 'WHERE' not in sql_query_list:
                sql_query_list[sql_query_list.index('AND')] = 'WHERE'

                sql_query = ' '.join(sql_query_list)
        except:
            None

        print(sql_query, "sql_query FINAL")

        sql_query_word = sql_query

        dict_chars_replace = {'open parenthesis': '(', 'close_parenthesis': ')', ' comma': ',', 'greater than or equal': '>=', 'greater than': '>', 'less than or equal': '<=',
        'less than': '<', 'not equal': '!=', 'equal': '=', 'hyphen': '-', 'apostrophe': "'", 'dummy': '*'}

        try:
            for key, value in dict_chars_replace.items():
                sql_query = sql_query.replace(key, value)
        except:
            pass
        
        if 'SELECT' in sql_query:
            try:
                self.ids.output_query_txtinput.foreground_color = 0, 1, 0, 1
                self.ids.output_query_txtinput.text = sql_query
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

        threading.Thread(target=self.thread_run_tts, args=(sql_query_word,), daemon=True).start()

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

        threading.Thread(target=self.thread_run_tts, args=(sql_query_word,), daemon=True).start()


class MainApp(App):    
    def build(self):
        return KVBL()

if __name__ == '__main__':
    MainApp().run()
