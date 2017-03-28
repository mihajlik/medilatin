# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import sqlite3
import tabulate

class CREATE_TABLE:

    def __init__(self):
        ## Connect to database.
        self.conn = sqlite3.connect('results.sqlite')
        self.cur = self.conn.cursor()
        tabulate.LATEX_ESCAPE_RULES={}

    def query_tu_al_sl_pl(self,training_unit,am_language,speaker_language,paragraph_language):
        self.cur.execute('''SELECT id FROM TrainingUnit WHERE training_unit = ? ''', (training_unit, ))
        training_unit_id = self.cur.fetchone()[0]
        self.cur.execute('''SELECT id FROM AMLanguage WHERE am_language = ? ''', (am_language, ))
        am_language_id = self.cur.fetchone()[0]
        self.cur.execute('''SELECT id FROM SpeakerLanguage WHERE speaker_language = ? ''', (speaker_language, ))
        speaker_language_id = self.cur.fetchone()[0]
        self.cur.execute('''SELECT id FROM ParagraphLanguage WHERE paragraph_language = ? ''', (paragraph_language, ))
        paragraph_language_id = self.cur.fetchone()[0]
        ## TODO: merge SK speaker id.
        self.cur.execute('''SELECT wer FROM AllResults
                WHERE am_language_id = ?
                AND training_unit_id = ?
                AND speaker_language_id = ?
                AND paragraph_language_id = ? ''', (am_language_id,training_unit_id,speaker_language_id,paragraph_language_id,))
        results = [item for sublist in self.cur.fetchall() for item in sublist]
        average_wer = round(sum(results) / len(results),1)

        return average_wer

    def write_table(self,am_language,training_unit):
        outname = '%s_%s' % (am_language.lower(),training_unit.lower())
        speaker_languages = ['CZ','HU','PL']
        paragraph_languages = ['CZ','HU','PL']
        table = [['Native Language','CZ','HU','PL']]
        for speaker_language in speaker_languages:
            row = []
            row.append(speaker_language)
            for paragraph_language in paragraph_languages:
                wer = self.query_tu_al_sl_pl(training_unit,am_language,speaker_language,paragraph_language)
                row.append(wer)
            table.append(row)
            
        with open('../paper/tables/%s.tex' % outname,'w',encoding='utf-8') as outf:
            outf.write(tabulate.tabulate(table,headers="firstrow",tablefmt="latex"))

    def query_db(self,training_unit,am_language):
        lt = 'LT'
        self.cur.execute('''SELECT id FROM TrainingUnit WHERE training_unit = ? ''', (training_unit, ))
        training_unit_id = self.cur.fetchone()[0]
        self.cur.execute('''SELECT id FROM AMLanguage WHERE am_language = ? ''', (am_language, ))
        am_language_id = self.cur.fetchone()[0]
        self.cur.execute('''SELECT id FROM SpeakerLanguage WHERE speaker_language = ? ''', (lt, ))
        speaker_language_id = self.cur.fetchone()[0]
        self.cur.execute('''SELECT wer FROM AllResults
                WHERE am_language_id = ?
                AND training_unit_id = ?
                AND speaker_language_id != ? ''', (am_language_id,training_unit_id,lt ))
        pl_grapheme_results = [item for sublist in self.cur.fetchall() for item in sublist]
        print(pl_grapheme_results)
        print(round(sum(pl_grapheme_results) / len(pl_grapheme_results),1))

if __name__ == '__main__':
    table_hu_phoneme = CREATE_TABLE()
    ## Extract HU PHONEME results.
    training_unit = 'PHONEME'
    am_language = 'HU'
    table_hu_phoneme.write_table(am_language,training_unit)

    table_hu_phoneme.cur.close()
    table_hu_phoneme.conn.close()