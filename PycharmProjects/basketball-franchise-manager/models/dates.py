class Dates:
    date_id = 0
    date_text = ''
    day = 0
    month = 0
    year = 0
    half = 0
    quarter = 0
    week = 0

    def __init__(self, date_id: int, date_text: str, day: int, month: int, year: int, half: int, quarter: int,
                 week: int):
        self.date_id = date_id
        self.date_text = date_text
        self.day = day
        self.month = month
        self.year = year
        self.half = half
        self.quarter = quarter
        self.week = week
