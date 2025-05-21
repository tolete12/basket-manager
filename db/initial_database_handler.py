from db.createrecords.create_dates import CreateDates
from utilities import Utilities
from variables.paths import ctlDir
import os
import utilities


class InitialDatabaseHandler:
    db_obj = None
    utilities = None
    sql_helper = None

    def __init__(self, db_obj, util, sql_helper):
        self.db_obj = db_obj
        self.utilities = util
        self.sql_helper = sql_helper

    def create_tables(self):
        for filename in os.listdir(ctlDir):
            self.db_obj.execute_query(Utilities.get_ctl_data(ctlDir, filename))
            self.db_obj.commit_db()

    def insert_default_records(self, start_year, end_year):
        queries_list = self.utilities.get_default_queries()
        if queries_list:
            self.db_obj.insert_records(queries_list)
        c = CreateDates(self.db_obj, self.sql_helper)
        c.generate_dates(start_year, end_year, True)
        self.db_obj.commit_db()
