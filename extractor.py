from datetime import date, datetime, timedelta
import requests
import random
import sqlite3


class Extractor:

    def __init__(self):
        self.date = str(date.today())
        self.response = {}
        self.definition = []
        self.example = []
        self.json = {}
        self.storage = self.get_definition

    def get_definition(self, input_word):
        url = f'https://api.dictionaryapi.dev/api/v2/entries/en/{input_word}'
        response = requests.get(url)
        with sqlite3.connect("database.db") as connect:
            cursor = connect.cursor()
            cursor.execute('''
                                SELECT COUNT (*) FROM vocabulary WHERE word = ?
                            ''', (input_word.upper(), ))
            result = cursor.fetchone()
            if result[0] > 0:
                return "Word already in dictionary"
            elif response.status_code == 200:
                self.response = response.json()
                word = input_word.upper()
                record_date = self.date
                try:
                    phonetics = self.response[0]['phonetic']
                except KeyError:
                    phonetics = "not found"
                definition = self.response[0]['meanings'][0]['definitions'][0]['definition']
                try:
                    example = self.response[0]['meanings'][0]['definitions'][0]['example']
                except KeyError:
                    example = "No example found."
                increment = 1
                return record_date, word, phonetics, definition, example, increment
            else:
                return "Unable to find"

    def save_word(self, array):
        if len(array) == 6:
            with sqlite3.connect("database.db") as connection:
                cursor = connection.cursor()
                cursor.execute('''
                                   INSERT INTO vocabulary (date, word, phonetics, definition, example, increment)
                                   VALUES (?, ?, ?, ?, ?, ?);
                               ''', (array[0], array[1], array[2], array[3], array[4], array[5]))
        else:
            print(array)

    def create_database(self):
        with sqlite3.connect("database.db") as connect:
            cursor = connect.cursor()
            cursor.execute('''
                            CREATE TABLE IF NOT EXISTS oxford3000
                            (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            date TEXT,
                            word TEXT,
                            phonetics TEXT,
                            definition TEXT,
                            example TEXT,
                            increment INT
                            )
                        ''')

    def create_clean_data_table(self):
        with sqlite3.connect("database.db") as connect:
            cursor = connect.cursor()
            cursor.execute('''
                        CREATE TABLE IF NOT EXISTS words_for_today
                        (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        date TEXT,
                        word TEXT,
                        phonetics TEXT,
                        definition TEXT,
                        example TEXT
                        )
                    ''')


    def pull_random_card(self):
        with sqlite3.connect("database.db") as connect:
            cursor = connect.cursor()
            cursor.execute('''
                            SELECT  id FROM vocabulary WHERE date <= ?
                        ''', (date.today(), ))
            result = cursor.fetchall()

            if not result:
                raise ValueError("No cards available for the given date condition.")

            random_word_id = random.choice(result)[0]
        return random_word_id

    def make_card(self, card_id):
        with sqlite3.connect("database.db") as connect:
            cursor = connect.cursor()
            cursor.execute('''
                        SELECT * FROM vocabulary WHERE id = ? AND date <= ?
                            ''', (card_id, date.today()))
            row = cursor.fetchall()

            word_title = row[0][2]
            word_phonetics = row[0][3]
            word_definition = row[0][4]
            word_example = row[0][5]

        return word_title, word_phonetics, word_definition, word_example

    def easy_scale(self, word):
        with sqlite3.connect("database.db") as connect:
            easy_increment = 3
            cursor = connect.cursor()
            cursor.execute('''
                            SELECT increment FROM vocabulary WHERE word = ?
                        ''', (word, ))

            current_day_count = cursor.fetchone()
            days_to_add = current_day_count[0] * easy_increment

            cursor.execute('''
                            UPDATE vocabulary
                            SET increment = ?
                            WHERE word = ?
                        ''', (days_to_add, word))

            connect.commit()

            date_object = datetime.strptime(self.date, "%Y-%m-%d")
            new_date_object = date_object + timedelta(days=days_to_add)
            new_date_string = new_date_object.strftime("%Y-%m-%d")

            cursor.execute('''
                            UPDATE vocabulary
                            SET date = ?
                            WHERE word = ?
                        ''', (new_date_string, word))

            connect.commit()


    def medium_scale(self, word):
        with sqlite3.connect("database.db") as connect:
            medium_increment = 1
            cursor = connect.cursor()
            cursor.execute('''
                            SELECT increment FROM vocabulary WHERE word = ?
                        ''', (word,))

            current_day_count = cursor.fetchone()
            days_to_add = current_day_count[0] * medium_increment

            cursor.execute('''
                            UPDATE vocabulary
                            SET increment = ?
                            WHERE word = ?
                        ''', (days_to_add, word))

            connect.commit()

            date_object = datetime.strptime(self.date, "%Y-%m-%d")
            new_date_object = date_object + timedelta(days=days_to_add)
            new_date_string = new_date_object.strftime("%Y-%m-%d")

            cursor.execute('''
                            UPDATE vocabulary
                            SET date = ?
                            WHERE word = ?
                        ''', (new_date_string, word))

            connect.commit()

    def hard_scale(self, word):
        pass
