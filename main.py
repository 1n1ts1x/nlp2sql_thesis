from functools import partial
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

            tts.say('What is your query?')
            Clock.schedule_once(partial(self.update, 'What is your query?', 2), 0)
            tts.runAndWait()
            tts.stop()

            try:
                audio = r.listen(self.source)
                query = r.recognize_google(audio)    

                tts.say('You said')
                Clock.schedule_once(partial(self.update, 'You said', 1), 0)
                tts.runAndWait()
                tts.say(query)
                Clock.schedule_once(partial(self.update, query, 1), 0)
                tts.runAndWait()
                self.sqlquery = query
            except:                
                tts.say('Failed to generate SQL statement voice is unrecognizable')
                Clock.schedule_once(partial(self.update, 'Failed to generate SQL statement voice is unrecognizable', 0), 0)
                tts.runAndWait()
                

    def on_enter(self):
        input_query_txt = ' '.join(self.input_query.text.split())
        self.ids.output_query_txtinput.text = ''

        # input_query_txt = self.t2d.convert(input_query_txt)
        input_query_txt = input_query_txt.replace('greater than or equal', ' above equal')
        input_query_txt = input_query_txt.replace('larger than or equal', ' above equal')
        input_query_txt = input_query_txt.replace('bigger than or equal', ' above equal')
        input_query_txt = input_query_txt.replace('higher than or equal', ' above equal')
        input_query_txt = input_query_txt.replace('lesser than or equal', ' below equal')
        input_query_txt = input_query_txt.replace('smaller than or equal', ' below equal')
        input_query_txt = input_query_txt.replace('less than or equal', ' below equal')
        input_query_txt = input_query_txt.replace('lower than or equal', ' below equal')
        input_query_txt = input_query_txt.replace('on the condition', ' where')
        input_query_txt = input_query_txt.replace('on the assumption', ' where')
        input_query_txt = input_query_txt.replace('beyond or over', ' above')
        input_query_txt = input_query_txt.replace('beyond or over', ' above')
        input_query_txt = input_query_txt.replace('over and beyond', ' above')
        input_query_txt = input_query_txt.replace('over and beyond', ' above')
        input_query_txt = input_query_txt.replace('on or before', ' below equal')
        input_query_txt = input_query_txt.replace('on or after', ' above equal')
        input_query_txt = input_query_txt.replace('before or on', ' below equal')
        input_query_txt = input_query_txt.replace('after or on', ' above equal')
        input_query_txt = input_query_txt.replace('each and every', ' all')
        input_query_txt = input_query_txt.replace('this day', ' today')
        input_query_txt = input_query_txt.replace('in which', ' where')
        input_query_txt = input_query_txt.replace('at which', ' where')
        input_query_txt = input_query_txt.replace('higher than', ' above')
        input_query_txt = input_query_txt.replace('greater than', ' above')
        input_query_txt = input_query_txt.replace('larger than', ' below')
        input_query_txt = input_query_txt.replace('bigger than', ' above')
        input_query_txt = input_query_txt.replace('lesser than', ' below')
        input_query_txt = input_query_txt.replace('smaller than', ' below')
        input_query_txt = input_query_txt.replace('less than', ' below')
        input_query_txt = input_query_txt.replace('lower than', ' below')
        input_query_txt = input_query_txt.replace('every single', ' all')
        input_query_txt = input_query_txt.replace('°', ' degree')
        input_query_txt = input_query_txt.replace('degrees', ' degree')
        input_query_txt = input_query_txt.replace('%', ' percent')
        input_query_txt = input_query_txt.replace('greater', ' above')
        input_query_txt = input_query_txt.replace('larger', ' above')
        input_query_txt = input_query_txt.replace('higher', ' above')
        input_query_txt = input_query_txt.replace('over', ' above')
        input_query_txt = input_query_txt.replace('beyond', ' above')
        input_query_txt = input_query_txt.replace('exceeding', ' above')
        input_query_txt = input_query_txt.replace('bigger', ' above')
        input_query_txt = input_query_txt.replace('exceeds', ' above')
        input_query_txt = input_query_txt.replace('exceed', ' above')
        input_query_txt = input_query_txt.replace('after', ' above')
        input_query_txt = input_query_txt.replace('lesser', ' below')
        input_query_txt = input_query_txt.replace('less', ' below')
        input_query_txt = input_query_txt.replace('smaller', ' below')
        input_query_txt = input_query_txt.replace('lower', ' below')
        input_query_txt = input_query_txt.replace('before', ' below')
        input_query_txt = input_query_txt.replace('wherein', ' where')
        input_query_txt = input_query_txt.replace('which', ' where')
        input_query_txt = input_query_txt.replace('that', ' where')
        input_query_txt = input_query_txt.replace('whose', ' where')
        input_query_txt = input_query_txt.replace('if', ' where')
        input_query_txt = input_query_txt.replace('provided', ' where')
        input_query_txt = input_query_txt.replace('assuming', ' where')
        input_query_txt = input_query_txt.replace('supposing', ' where')
        input_query_txt = input_query_txt.replace('presuming', ' where')
        input_query_txt = input_query_txt.replace('that', ' where')
        input_query_txt = input_query_txt.replace('from', ' of')
        input_query_txt = input_query_txt.replace('each', ' all')
        input_query_txt = input_query_txt.replace('every', ' all')
        input_query_txt = input_query_txt.replace('entire', ' all')
        input_query_txt = input_query_txt.replace('everything', ' all')
        input_query_txt = input_query_txt.replace('check', ' show')
        input_query_txt = input_query_txt.replace('inspect', ' show')
        input_query_txt = input_query_txt.replace('scan', ' show')
        input_query_txt = input_query_txt.replace('readings', ' data')
        input_query_txt = input_query_txt.replace('reading', ' data')
        input_query_txt = re.sub(r'\bany of the parameters\b', ' show', input_query_txt)
        input_query_txt = re.sub(r'\bany of parameters\b', ' show', input_query_txt)
        input_query_txt = re.sub(r'\bany of the data\b', ' show', input_query_txt)
        input_query_txt = re.sub(r'\bany of data\b', ' show', input_query_txt)
        input_query_txt = re.sub(r'\bsee\b', ' show', input_query_txt)
        input_query_txt = re.sub(r'\bacquire\b', ' show', input_query_txt)
        input_query_txt = re.sub(r'\bobtain\b', ' show', input_query_txt)
        input_query_txt = re.sub(r'\bexhibit\b', ' show', input_query_txt)
        input_query_txt = re.sub(r'\bplants\b', 'table', input_query_txt)
        input_query_txt = re.sub(r'\bplant\b', 'table', input_query_txt)

        prep = CleanText(input_query_txt, self.save_for_later, True)
        t = TextAnalysis(prep.clean_text())

        try:
            t.parse_tokens()
        except:
            sql_gen = SQLGenerator(prep.clean_text(), tts, prep.lemmatized_tokens2)
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

        sql_query_word = sql_query

        dict_chars_replace = {' comma': ',', 'greater than or equal': '>=', 'greater than': '>', 'less than or equal': '<=',
        'less than': '<', 'not equal': '!=', 'equal': '=', 'hyphen': '-', 'apostrophe': "'", 'dummy': '*'}

        try:
            for key, value in dict_chars_replace.items():
                sql_query = sql_query.replace(key, value)
        except:
            pass
        
        sql_query_list = list(sql_query.split(' '))

        try:
            if 'AND' in sql_query_list and 'WHERE' not in sql_query_list:
                sql_query_list[sql_query_list.index('AND')] = 'WHERE'

                sql_query = ' '.join(sql_query_list)
        except:
            None

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
        input_query_txt = input_query_txt.replace('greater than or equal', ' above equal')
        input_query_txt = input_query_txt.replace('larger than or equal', ' above equal')
        input_query_txt = input_query_txt.replace('bigger than or equal', ' above equal')
        input_query_txt = input_query_txt.replace('higher than or equal', ' above equal')
        input_query_txt = input_query_txt.replace('lesser than or equal', ' below equal')
        input_query_txt = input_query_txt.replace('smaller than or equal', ' below equal')
        input_query_txt = input_query_txt.replace('less than or equal', ' below equal')
        input_query_txt = input_query_txt.replace('lower than or equal', ' below equal')
        input_query_txt = input_query_txt.replace('on the condition', ' where')
        input_query_txt = input_query_txt.replace('on the assumption', ' where')
        input_query_txt = input_query_txt.replace('beyond or over', ' above')
        input_query_txt = input_query_txt.replace('beyond or over', ' above')
        input_query_txt = input_query_txt.replace('over and beyond', ' above')
        input_query_txt = input_query_txt.replace('over and beyond', ' above')
        input_query_txt = input_query_txt.replace('on or before', ' below equal')
        input_query_txt = input_query_txt.replace('on or after', ' above equal')
        input_query_txt = input_query_txt.replace('before or on', ' below equal')
        input_query_txt = input_query_txt.replace('after or on', ' above equal')
        input_query_txt = input_query_txt.replace('each and every', ' all')
        input_query_txt = input_query_txt.replace('this day', ' today')
        input_query_txt = input_query_txt.replace('in which', ' where')
        input_query_txt = input_query_txt.replace('at which', ' where')
        input_query_txt = input_query_txt.replace('higher than', ' above')
        input_query_txt = input_query_txt.replace('greater than', ' above')
        input_query_txt = input_query_txt.replace('larger than', ' below')
        input_query_txt = input_query_txt.replace('bigger than', ' above')
        input_query_txt = input_query_txt.replace('lesser than', ' below')
        input_query_txt = input_query_txt.replace('smaller than', ' below')
        input_query_txt = input_query_txt.replace('less than', ' below')
        input_query_txt = input_query_txt.replace('lower than', ' below')
        input_query_txt = input_query_txt.replace('every single', ' all')
        input_query_txt = input_query_txt.replace('°', ' degree')
        input_query_txt = input_query_txt.replace('degrees', ' degree')
        input_query_txt = input_query_txt.replace('%', ' percent')
        input_query_txt = input_query_txt.replace('greater', ' above')
        input_query_txt = input_query_txt.replace('larger', ' above')
        input_query_txt = input_query_txt.replace('higher', ' above')
        input_query_txt = input_query_txt.replace('over', ' above')
        input_query_txt = input_query_txt.replace('beyond', ' above')
        input_query_txt = input_query_txt.replace('exceeding', ' above')
        input_query_txt = input_query_txt.replace('bigger', ' above')
        input_query_txt = input_query_txt.replace('exceeds', ' above')
        input_query_txt = input_query_txt.replace('exceed', ' above')
        input_query_txt = input_query_txt.replace('after', ' above')
        input_query_txt = input_query_txt.replace('lesser', ' below')
        input_query_txt = input_query_txt.replace('less', ' below')
        input_query_txt = input_query_txt.replace('smaller', ' below')
        input_query_txt = input_query_txt.replace('lower', ' below')
        input_query_txt = input_query_txt.replace('before', ' below')
        input_query_txt = input_query_txt.replace('wherein', ' where')
        input_query_txt = input_query_txt.replace('which', ' where')
        input_query_txt = input_query_txt.replace('that', ' where')
        input_query_txt = input_query_txt.replace('whose', ' where')
        input_query_txt = input_query_txt.replace('if', ' where')
        input_query_txt = input_query_txt.replace('provided', ' where')
        input_query_txt = input_query_txt.replace('assuming', ' where')
        input_query_txt = input_query_txt.replace('supposing', ' where')
        input_query_txt = input_query_txt.replace('presuming', ' where')
        input_query_txt = input_query_txt.replace('that', ' where')
        input_query_txt = input_query_txt.replace('from', ' of')
        input_query_txt = input_query_txt.replace('each', ' all')
        input_query_txt = input_query_txt.replace('every', ' all')
        input_query_txt = input_query_txt.replace('entire', ' all')
        input_query_txt = input_query_txt.replace('everything', ' all')
        input_query_txt = input_query_txt.replace('check', ' show')
        input_query_txt = input_query_txt.replace('inspect', ' show')
        input_query_txt = input_query_txt.replace('scan', ' show')
        input_query_txt = input_query_txt.replace('readings', ' data')
        input_query_txt = input_query_txt.replace('reading', ' data')
        input_query_txt = re.sub(r'\bany of the parameters\b', ' show', input_query_txt)
        input_query_txt = re.sub(r'\bany of parameters\b', ' show', input_query_txt)
        input_query_txt = re.sub(r'\bany of the data\b', ' show', input_query_txt)
        input_query_txt = re.sub(r'\bany of data\b', ' show', input_query_txt)
        input_query_txt = re.sub(r'\bsee\b', ' show', input_query_txt)
        input_query_txt = re.sub(r'\bacquire\b', ' show', input_query_txt)
        input_query_txt = re.sub(r'\bobtain\b', ' show', input_query_txt)
        input_query_txt = re.sub(r'\bexhibit\b', ' show', input_query_txt)
        input_query_txt = re.sub(r'\bplants\b', 'table', input_query_txt)
        input_query_txt = re.sub(r'\bplant\b', 'table', input_query_txt)
        input_query_txt = input_query_txt.replace('lakhs', ' lux')
        input_query_txt = input_query_txt.replace('lakhs', ' lux')
        input_query_txt = input_query_txt.replace('looks', ' lux')
        input_query_txt = input_query_txt.replace('blocks', ' lux')
        input_query_txt = input_query_txt.replace('bpm', ' ppm')

        
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

        sql_query_word = sql_query

        dict_chars_replace = {' comma': ',', 'greater than or equal': '>=', 'greater than': '>', 'less than or equal': '<=',
        'less than': '<', 'not equal': '!=', 'equal': '=', 'hyphen': '-', 'apostrophe': "'", 'dummy': '*'}

        try:
            for key, value in dict_chars_replace.items():
                sql_query = sql_query.replace(key, value)
        except:
            pass

        sql_query_list = list(sql_query.split(' '))

        try:
            if 'AND' in sql_query_list and 'WHERE' not in sql_query_list:
                sql_query_list[sql_query_list.index('AND')] = 'WHERE'

                sql_query = ' '.join(sql_query_list)
        except:
            None

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

