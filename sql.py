import mysql.connector
from mysql.connector import Error
import matplotlib.pyplot as plt
from data_model import *

class SQL:
    def __init__(self, isGraphSql=False, isGoodCondition=False, isGoodConditionDate=False, isGoodOrBadConditionDate=False):
        self.isGraphSql = isGraphSql
        self.isGoodCondition = isGoodCondition
        self.isGoodConditionDate = isGoodConditionDate
        self.isGoodOrBadConditionDate = isGoodOrBadConditionDate
        self.text = ''
        self.trec = TableRecord()
        self.col_name = []
        self.col_val = []
        self.pair = []

    def execute_query(self, query):
        con = mysql.connector.connect(host='localhost', database='plant', username='root', password='')
        
        try:
            cur = con.cursor()
            cur.execute(query)
            column_names = [desc[0] for desc in cur.description]
            records = cur.fetchall()
            print("Record count: ", cur.rowcount)
            
            if self.isGraphSql:
                y = []
                dates = []

                try:
                    for row in records:
                        dates.append(row[1])
                        y.append(row[2])

                    plt.plot_date(dates, y, 'g')
                    plt.xticks(rotation=70)
                    plt.show()
                except:
                    pass
            elif self.isGoodConditionDate:
                records_list = []
                for row in records:
                    records_list.append(row[0])
                    records_list.append(row[1])
                    records_list.append(row[2])
                    print("Date_n_Time =>", row[0])
                    print("parameter =>", row[1])
                    print("value =>", row[2])

                result = ""

                for i, item in enumerate(records_list, 1):
                    result += str(item)
                    if not (i % 3):
                        result += "\n"
                    else:
                        result += ", "

                # For mod
                for row in records:
                    for column, value in zip(column_names, row):
                        print(column, value)
                        self.trec[column] = value

                for key, value in self.trec.data.items():
                    self.col_name.append(key)
                    self.col_val.append(value)


                mod_list = list(zip(*self.col_val))
                res_list = [list(mod) for mod in mod_list]

                self.pair = FieldValue(_key=self.col_name, _value=res_list)
                
                if not cur.rowcount:
                    return f"There are {cur.rowcount} records showing this plant does {'not' if self.isGoodOrBadConditionDate else ''} have optimal conditions."
                elif cur.rowcount < 2:
                    return f"There is {cur.rowcount} record showing this plant does {'not' if self.isGoodOrBadConditionDate else ''} have optimal conditions.\n\nHere is the list:\n" + result
                else:
                    return f"There are {cur.rowcount} records showing this plant does {'not' if self.isGoodOrBadConditionDate else ''} have optimal conditions.\n\nHere is the list:\n" + result
            elif self.isGoodCondition:
                records_list = []
                for row in records:
                    records_list.append(row[0])
                    records_list.append(row[1])
                    records_list.append(row[2])
                    records_list.append(row[3])
                    records_list.append(row[4])
                    print("count_temperature =>", row[0])
                    print("count_humidity =>", row[1])
                    print("count_soil =>", row[2])
                    print("count_air =>", row[3])
                    print("count_light =>", row[4])
                
                if sum(records_list) == len(records_list):
                    self.text = "Yes, all parameters have been met."
                else:
                    params_cond = []

                    if not records_list[0]:
                        params_cond.append("temperature")
                    if not records_list[1]:
                        params_cond.append("humidity")
                    if not records_list[2]:
                        params_cond.append("soil moisture")
                    if not records_list[3]:
                        params_cond.append("air quality")
                    if not records_list[4]:
                        params_cond.append("light intensity")
        
                    if len(params_cond) > 1:
                        txt = ''
                        params_cond.insert(len(params_cond) - 1, "and")
                        txt = ', '.join(params_cond)
                        self.text = txt.replace("and,", "and" )

                    self.text = f"No, {self.text} did not meet the ideal condition."

                # For mod
                for row in records:
                    for column, value in zip(column_names, row):
                        print(column, value)
                        self.trec[column] = value

                for key, value in self.trec.data.items():
                    self.col_name.append(key)
                    self.col_val.append(value)


                mod_list = list(zip(*self.col_val))
                res_list = [list(mod) for mod in mod_list]

                self.pair = FieldValue(_key=self.col_name, _value=res_list)
 
                return self.text
            
            for row in records:
                for column, value in zip(column_names, row):
                    print(column, value)
                    self.trec[column] = value

            for key, value in self.trec.data.items():
                self.col_name.append(key)
                self.col_val.append(value)


            mod_list = list(zip(*self.col_val))
            res_list = [list(mod) for mod in mod_list]

            self.pair = FieldValue(_key=self.col_name, _value=res_list)

        except Error as error:
            print("Error in the program {}".format(error))
        finally:
            if con.is_connected():
                cur.close()
                con.close()
                print("MySQL Connection is now CLOSED!")

