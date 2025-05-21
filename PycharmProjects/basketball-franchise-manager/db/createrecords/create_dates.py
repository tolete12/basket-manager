import datetime

from db.sql_lite_handler import SQLiteHandler
from db.sql_lite_helper import SQLLiteHelper
from models.dates import Dates
from utilities import Utilities
from variables.constants import DATE_ID, DATES


class CreateDates:
    def __init__(self, db_obj: SQLiteHandler, sql_helper: SQLLiteHelper):
        self.db_obj = db_obj
        self.sql_helper = sql_helper

    def generate_dates(self, start_year: int, end_year: int, insert_db: True):
        list_dates = []
        for year in range(start_year, end_year + 1):
            first_day = datetime.date(year, 1, 1)
            last_day = datetime.date(year, 12, 31)
            day = datetime.timedelta(days=1)
            date_id = self.sql_helper.get_max_id(DATE_ID, DATES)
            while first_day <= last_day:
                date_id += 1
                text_date = Utilities.convert_date_to_text(first_day)
                half = 1 if first_day.month <= 6 else 2
                quarter = (first_day.month - 1) // 3 + 1

                values = [date_id,
                          text_date,
                          first_day.day,
                          first_day.month,
                          first_day.year,
                          half,
                          quarter,
                          first_day.isocalendar()[1]]

                list_dates.append(
                    Dates(date_id, text_date, first_day.day, first_day.month, first_day.year, half, quarter,
                          first_day.isocalendar()[1]))
                if insert_db:
                    self.sql_helper.insert_records_handler("DATES", values)

                first_day = first_day + day
        if insert_db:
            self.db_obj.commit_db()
        return list_dates
