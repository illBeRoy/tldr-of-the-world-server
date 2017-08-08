# Script used for transferring the pantheon csv dataset into an sqlite db
import os
import sqlite3
import csv


class CsvToSqlite(object):
    def __init__(self, csv_path, sqlite_path):
        self._sqlite_path = sqlite_path
        self._csv_path = csv_path
        self._conn = self._init_db(sqlite_path)
        self._insert_data_from_csv()

    def _insert_data_from_csv(self):
        with open(self._csv_path, 'r', encoding='utf8') as input_file:
            reader = csv.reader(input_file, delimiter=',')
            cur = self._conn.cursor()

            # skip first row (headings)
            row = next(reader)

            already_in = []
            for row in reader:
                wikiquote_name = row[23]
                wikipedia_names = row[24]
                occupation = row[13]
                industry = row[14]
                domain = row[15]
                gender = row[12]
                birthyear = row[11]
                lat = row[8]
                lon = row[9]
                countryName = row[5]
                birthcity = row[3]

                cur.execute('INSERT INTO people (wikiquote_name,'
                            'wikipedia_name,'
                            'occupation,'
                            'industry,'
                            'domain,'
                            'gender,'
                            'birthyear,'
                            'LAT,'
                            'LON,'
                            'countryName,'
                            'birthcity) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                            (wikiquote_name, wikipedia_names, occupation, industry, domain, gender, birthyear, lat,
                             lon, countryName, birthcity))

            self._conn.commit()

    def _init_db(self, sqlite_path):
        '''
        Initializes sqlite
        '''
        if os.path.exists(sqlite_path):
            conn = sqlite3.connect(sqlite_path)
        else:
            conn = sqlite3.connect(sqlite_path)
            conn.execute('CREATE TABLE people (wikiquote_name TEXT PRIMARY KEY,'
                         'wikipedia_name TEXT,'
                         'occupation TEXT,'
                         'industry TEXT,'
                         'domain TEXT,'
                         'gender TEXT,'
                         'birthyear TEXT,'
                         'LAT TEXT,'
                         'LON TEXT,'
                         'countryName TEXT,'
                         'birthcity TEXT)')
            conn.commit()

        return conn

if __name__ == '__main__':
    db_creator = CsvToSqlite('pantheon_final.csv', 'people.sqlite')
