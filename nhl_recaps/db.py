#/usr/bin/env python
"""database-related functions"""

import sqlite3
import hashlib

class RecapDb:
    """builds and writes to db"""

    def __init__(self, db_location):
        self.values = ['date', 'home', 'away', 'description', 'score', 'checksum']
        self.conn = sqlite3.connect(db_location)
        self.c = self.conn.cursor()
        self.build_schema()

    def build_schema(self):
        try:
            self.c.execute('''CREATE TABLE IF NOT EXISTS recaps
                 (date text, home text, away text, description text, score text, checksum text)''')
            self.conn.commit()
        except:
            print('table already exists')

    def insert_value(self, value):
        """value field should be a dictionary w/ any number of values. ex ('home', 'ANA')"""
        checksum = data.hash(value)

        self.c.executemany('INSERT INTO recaps VALUES (?,?,?,?,?,?)', value)
        self.conn.commit()

    def hash(self, string):
        """pass a string through and obtain a hash."""
        hash = hashlib.md5(b'hello')

        return hash.hexdigest()


if __name__ == '__main__':
    data = RecapDb('recaps.db')
    checksum = data.hash('hello worls')
    data.insert_value([('11/1/2018', 'ducks', 'rangers', 'sad game', '3-2', checksum)])
