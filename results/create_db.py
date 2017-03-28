# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import sqlite3

class CREATEDB:

    def __init__(self):
        ## Connect to database.
        self.conn = sqlite3.connect('results.sqlite')
        self.cur = self.conn.cursor()

        ## Create tables.
        self.cur.execute('DROP TABLE IF EXISTS AMLanguage')
        self.cur.execute('DROP TABLE IF EXISTS SpeakerLanguage')
        self.cur.execute('DROP TABLE IF EXISTS ParagraphLanguage')
        self.cur.execute('DROP TABLE IF EXISTS TrainingUnit')
        self.cur.execute('DROP TABLE IF EXISTS AllResults')

        self.cur.execute('''CREATE TABLE AMLanguage (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                am_language TEXT UNIQUE
                )''')
        self.cur.execute('''CREATE TABLE SpeakerLanguage (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                speaker_language TEXT UNIQUE
                )''')
        self.cur.execute('''CREATE TABLE ParagraphLanguage (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                paragraph_language TEXT UNIQUE
                )''')
        self.cur.execute('''CREATE TABLE TrainingUnit (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                training_unit TEXT UNIQUE
                )''')

        self.cur.execute('''CREATE TABLE AllResults (
                am_language_id INTEGER,
                speaker_language_id INTEGER,
                paragraph_language_id INTEGER,
                training_unit_id INTEGER,
                wer REAL,
                PRIMARY KEY (am_language_id,speaker_language_id,paragraph_language_id,training_unit_id,wer)
                )''')

    def add_to_all_data(self,am_language,speaker_language,paragraph_language,training_unit,wer):
        self.cur.execute('''INSERT OR IGNORE INTO AMLanguage (am_language)
                        VALUES (?) ''', (am_language,))
        self.cur.execute('SELECT id FROM AMLanguage WHERE am_language = ? ', (am_language, ))
        am_language_id = self.cur.fetchone()[0]

        self.cur.execute('''INSERT OR IGNORE INTO SpeakerLanguage (speaker_language)
                VALUES (?)''', (speaker_language,))
        self.cur.execute('SELECT id FROM SpeakerLanguage WHERE speaker_language = ? ', (speaker_language, ))
        speaker_language_id = self.cur.fetchone()[0]

        self.cur.execute('''INSERT OR IGNORE INTO ParagraphLanguage (paragraph_language)
                VALUES (?)''', (paragraph_language,))
        self.cur.execute('SELECT id FROM ParagraphLanguage WHERE paragraph_language = ? ', (paragraph_language, ))
        paragraph_language_id = self.cur.fetchone()[0]

        self.cur.execute('''INSERT OR IGNORE INTO TrainingUnit (training_unit)
                VALUES (?)''', (training_unit,))
        self.cur.execute('SELECT id FROM TrainingUnit WHERE training_unit = ? ', (training_unit, ))
        training_unit_id = self.cur.fetchone()[0]

        #print(am_language_id,speaker_language_id,paragraph_language_id,training_unit_id,wer)

        self.cur.execute('''INSERT OR REPLACE INTO AllResults
                (am_language_id,speaker_language_id,paragraph_language_id,training_unit_id,wer) VALUES (?,?,?,?,?)''',
                (am_language_id,speaker_language_id,paragraph_language_id,training_unit_id,wer))

        self.conn.commit()

    def extract_record_name(self,record_name):
        ## Get speaker language.
        if 'CS' in record_name:
            speaker_language = 'CZ'
        elif 'HU' in record_name:
            speaker_language = 'HU'
        elif 'LT' in record_name:
            speaker_language = 'LT'
        elif 'PL' in record_name:
            speaker_language = 'PL'
        elif 'SK' in record_name:
            speaker_language = 'SK'
        else:
            speaker_language = None

        ## Get paragraph language.
        if 'Fridericus' in record_name:
            paragraph_language = 'PL'
        elif 'Nicolaus' in record_name:
            paragraph_language = 'HU'
        elif 'Wencezlaus' in record_name:
            paragraph_language = 'CZ'
        else:
            paragraph_language = None

        return speaker_language, paragraph_language

    def extract_filename(self,fn):
        ## Get AM language.
        am_language_list = [] 
        if 'CZ' in fn:
            am_language_list.append('CZ')
        if 'HU' in fn:
            am_language_list.append('HU')
        if 'RO' in fn:
            am_language_list.append('RO')
        if 'PL' in fn:
            am_language_list.append('PL')

        am_language = '_'.join(am_language_list)

        ## Get training unit.
        if 'USG' in fn:
            training_unit = 'USG'
        elif 'PHONEME' in fn:
            training_unit = 'PHONEME'
        else:
            training_unit = 'GRAPHEME'

        return am_language, training_unit

    def readin(self,fn):
        am_language,training_unit = self.extract_filename(fn)
        c = 0
        with open(fn,encoding='utf-8') as inf:
            for line in inf:
                if c > 0:
                    ll = line.split()
                    if ll == []:
                        break
                    record_name = ll[0]
                    speaker_language,paragraph_language = self.extract_record_name(record_name)
                    wer = ll[5]
                    self.add_to_all_data(am_language,speaker_language,paragraph_language,training_unit,wer)
                c += 1

if __name__ == '__main__':
    wers = CREATEDB()
    import glob
    for fn in glob.iglob('*.log'): 
        if 'paragraph' in fn:
            wers.readin(fn)

    wers.cur.close()
    wers.conn.close()
