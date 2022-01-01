import sqlite3
from get_information import *

sqlite_connection = sqlite3.connect("user.bd")
cursor = sqlite_connection.cursor()

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
    cursor.execute(sqlite_create_table_query)
    sqlite_connection.commit()

def write_schedule(login, password, my_range, first_time):

    def make_text(item):
        if item == []:
            text = 'В этот день нет занятий'
        else:
            index = -1
            text = ""
            for lesson in item:
                if int(lesson[0]) != index:
                    index += 1
                    text += "-----\n" + f"{index + 1} пара: {lesson[1]}\n"
                text += f"{lesson[2]};{lesson[3]};{lesson[5]};{str(lesson[4])};\n"
        text = text.replace("\'", "")
        return text

    days_schedule = authorization(login, password, my_range)
    texts = []
    if first_time:
        for item in days_schedule:
            texts.append(make_text(item))
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
        cursor.execute(sqlite_add_values_query)
        sqlite_connection.commit()
    else:
        cursor.execute("SELECT * FROM users_schedule WHERE login = ?", (login,))
        data = cursor.fetchall()[0]
        new_days_schedule = []
        for i in range(4, 14):
            new_days_schedule.append(data[i])
        new_days_schedule.append(make_text(days_schedule[0]))
        cursor.execute(f'''UPDATE users_schedule
            SET day_5 = '{new_days_schedule[0]}',
                day_4 = '{new_days_schedule[1]}',
                day_3 = '{new_days_schedule[2]}',
                day_2 = '{new_days_schedule[3]}',
                day_1 = '{new_days_schedule[4]}',
                day = '{new_days_schedule[5]}',
                day1 = '{new_days_schedule[6]}',
                day2 = '{new_days_schedule[7]}',
                day3 = '{new_days_schedule[8]}',
                day4 = '{new_days_schedule[9]}',
                day5 = '{new_days_schedule[10]}'
        WHERE id = {data[0]};''')
        sqlite_connection.commit()


# def check_new_user(login):
#     cursor.execute("SELECT rowid FROM users_schedule WHERE login = ?", (login, ))
#     data = cursor.fetchall()
#     if len(data) == 0:
#         return True
#     else:
#         return False