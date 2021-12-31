import sqlite3
from get_information import *

sqlite_connection = sqlite3.connect("user.bd")

def create_table():
    sqlite_create_table_query = '''CREATE TABLE users_schedule (
                                    id INTEGER PRIMARY KEY,
                                    login TEXT NOT NULL,
                                    password TEXT NOT NULL,
                                    day_5 TEXT NOT NULL,
                                    day_4 TEXT NOT NULL,
                                    day_3 TEXT NOT NULL,
                                    day_2 TEXT NOT NULL,
                                    day_1 TEXT NOT NULL,
                                    day TEXT NOT NULL,
                                    day1 TEXT NOT NULL,
                                    day2 TEXT NOT NULL,
                                    day3 TEXT NOT NULL,
                                    day4 TEXT NOT NULL,
                                    day5 TEXT NOT NULL);'''
    cursor = sqlite_connection.cursor()
    cursor.execute(sqlite_create_table_query)
    sqlite_connection.commit()

def write_schedule(login, password):
    days_schedule = authorization(login, password)
    texts = []
    for index, item in enumerate(days_schedule):
        if item == []:
            text = 'В этот день нет занятий'
        else:
            index = -1
            text = ""
            for lesson in item:
                if int(lesson[0]) != index:
                    index+= 1
                    text+= "-----\n" + f"{index+1} пара: {lesson[1]}\n"
                text+= f"{lesson[2]};{lesson[3]};{lesson[5]};{str(lesson[4])};\n"
        text = text.replace("\'","")
        texts.append(text)
    sqlite_add_values_query = f'''INSERT INTO users_schedule (
                               login,
                               password,
                               day_5,
                               day_4,
                               day_3,
                               day_2,
                               day_1,
                               day,
                               day1,
                               day2,
                               day3,
                               day4,
                               day5
                           )
                           VALUES (
                               '{login}',
                               '{password}',
                               '{texts[0]}',
                               '{texts[1]}',
                               '{texts[2]}',
                               '{texts[3]}',
                               '{texts[4]}',
                               '{texts[5]}',
                               '{texts[6]}',
                               '{texts[7]}',
                               '{texts[8]}',
                               '{texts[9]}',
                               '{texts[10]}'
                           );'''
    cursor = sqlite_connection.cursor()
    cursor.execute(sqlite_add_values_query)
    sqlite_connection.commit()

write_schedule("ggg003", "grig1001")