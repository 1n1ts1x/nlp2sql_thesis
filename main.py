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

Window.clearcolor = (.9, .9, .9, .9) 

tts = pyttsx3.init()
tts.setProperty('rate', 150)
    

class KVBL(BoxLayout):
    input_query = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(KVBL, self).__init__(**kwargs)
        self.save_for_later = []
        self.sqlquery = ''

    @mainthread 
    def update(self, q, *a):
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

    def back_to_main(self, q):
        self.update(q)
            
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
            tts.runAndWait()
            tts.stop()

            try:
                audio = r.listen(self.source)
                query = r.recognize_google(audio)    

                tts.say('You said')
                tts.runAndWait()
                tts.say(query)
                tts.runAndWait()
                self.sqlquery = query
            except:                
                tts.say('Failed to generate SQL statement voice is unrecognizable')
                tts.runAndWait()
                

    def on_enter(self):
        input_query_txt = ' '.join(self.input_query.text.split())
        self.ids.output_query_txtinput.text = ''
        
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
        input_query_txt = input_query_txt.replace('this day', ' today')
        input_query_txt = input_query_txt.replace('in which', ' where')
        input_query_txt = input_query_txt.replace('at which', ' where')
        input_query_txt = input_query_txt.replace('greater than', ' above')
        input_query_txt = input_query_txt.replace('larger than', ' below')
        input_query_txt = input_query_txt.replace('bigger than', ' above')
        input_query_txt = input_query_txt.replace('lesser than', ' below')
        input_query_txt = input_query_txt.replace('smaller than', ' below')
        input_query_txt = input_query_txt.replace('less than', ' below')
        input_query_txt = input_query_txt.replace('lower than', ' below')
        input_query_txt = input_query_txt.replace('°', ' degrees')
        input_query_txt = input_query_txt.replace('%', ' percent')
        input_query_txt = input_query_txt.replace('greater', ' above')
        input_query_txt = input_query_txt.replace('larger', ' above')
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
        input_query_txt = input_query_txt.replace('plant', ' table')
        input_query_txt = input_query_txt.replace('intesity', '')

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

        if 'SELECT' in sql_query:
            try:
                self.ids.output_query_txtinput.foreground_color = 0, 1, 0, 1
                self.ids.output_query_txtinput.text = sql_geni.query
            except:
                self.ids.output_query_txtinput.text = sql_gen.query
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
        
        threading.Thread(target=self.thread_run_tts, args=(sql_query,), daemon=True).start()

    def on_enter2(self):
        self.ids.input_query.text = ''
        self.ids.output_query_txtinput.text = ''


        query = ''
        t = threading.Thread(target=self.thread_run_stt, args=(query,), daemon=True)
        t.start()
        t.join()

        input_query_txt = self.sqlquery
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
        input_query_txt = input_query_txt.replace('this day', ' today')
        input_query_txt = input_query_txt.replace('in which', ' where')
        input_query_txt = input_query_txt.replace('at which', ' where')
        input_query_txt = input_query_txt.replace('greater than', ' above')
        input_query_txt = input_query_txt.replace('larger than', ' below')
        input_query_txt = input_query_txt.replace('bigger than', ' above')
        input_query_txt = input_query_txt.replace('lesser than', ' below')
        input_query_txt = input_query_txt.replace('smaller than', ' below')
        input_query_txt = input_query_txt.replace('less than', ' below')
        input_query_txt = input_query_txt.replace('lower than', ' below')
        input_query_txt = input_query_txt.replace('°', ' degrees')
        input_query_txt = input_query_txt.replace('%', ' percent')
        input_query_txt = input_query_txt.replace('greater', ' above')
        input_query_txt = input_query_txt.replace('larger', ' above')
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
        input_query_txt = input_query_txt.replace('plant', ' table')
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
        'less than': '<', 'not equal': '!=', 'equal': '=', 'hyphen': '-', 'apostrophe': "'"}

        try:
            for key, value in dict_chars_replace.items():
                sql_query = sql_query.replace(key, value)
        except:
            pass
        
        try:
            Clock.schedule_once(partial(self.update, sql_query), 0)
        finally:
            pass

        threading.Thread(target=self.thread_run_tts, args=(sql_query_word,), daemon=True).start()


class MainApp(App):    
    def build(self):
        return KVBL()

if __name__ == '__main__':
    MainApp().run()