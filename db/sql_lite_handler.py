import logging
import os
import sqlite3
from variables.paths import savegamesDir, parentDir


class SQLiteHandler(logging.Handler):  # Inherit from logging.Handler
    """
    Logging handler that write logs to SQLite DB
    """
    db = None

    def __init__(self, filename: str, override: bool = False, save_game: bool = False):
        # run the regular Handler __init__
        logging.Handler.__init__(self)

        try:
            # Create/Override database
            if save_game:
                if override and os.path.exists(savegamesDir + '/' + filename):
                    os.remove(savegamesDir + '/' + filename)
                self.db = sqlite3.connect(savegamesDir + '/' + filename)
            else:
                if override and os.path.exists(parentDir + '/' + filename):
                    os.remove(parentDir + '/' + filename)
                self.db = sqlite3.connect(parentDir + '/' + filename)  # might need to use self.filename
            self.db.row_factory = sqlite3.Row
        except sqlite3.Error as error:
            print("Error while connecting to sqlite", error)

    def insert_records_with_cursor(self, sql: str, list_values: list):
        self.db.cursor().execute(sql, list_values)

    def commit_db(self):
        self.db.commit()

    def execute_query(self, query):
        self.db.execute(query)

    def insert_records(self, records):
        for i in range(len(records)):
            # print(records[i])
            self.db.execute(records[i])

    def read_records(self, query):
        cursor_obj = self.db.cursor()
        cursor_obj.execute(query)
        rows = cursor_obj.fetchall()
        return rows, cursor_obj

    def read_records_filtered(self, field: str, table: str, fields_filtered: list = None, values_filtered: list = None,
                              fetchall: bool = True):
        if not field == "*":
            field += " AS VALUE "
        query = "SELECT " + field + " FROM " + table
        if fields_filtered and values_filtered:
            query += " WHERE "
            for index in range(len(fields_filtered)):
                if not index == 0:
                    query += " AND "
                query += fields_filtered[index] + " = " + (
                    str(values_filtered[index]) if isinstance(values_filtered[index], int) else '' + values_filtered[
                        index] + '')

        cursor_obj = self.db.cursor()

        if fetchall:
            row = cursor_obj.execute(query).fetchall()
        else:
            row = cursor_obj.execute(query).fetchone()
        return row

    def close_connection(self):
        self.db.close()


if __name__ == '__main__':
    # Create a logging object (after configuring logging)
    logger = logging.getLogger('someLoggerNameLikeDebugOrWhatever')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(SQLiteHandler('debugLog.sqlite'))
    logger.debug('Test 1')
    logger.warning('Some warning')
    logger.error('Alarma!')
