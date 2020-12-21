import pandas as pd
from datetime import datetime

from config import DATE_TIME


class CalenderService():
    def __init__(self):
        self.calendar = pd.read_csv('data/calendar.csv')

    def is_market_day(self, date_time) -> bool:
        temp = self.calendar[self.calendar[DATE_TIME] == date_time]
        if len(temp) == 1:
            return bool(temp['is_market_day'])
        elif len(temp) > 1:
            raise ValueError('[ERROR] data not clean - duplicate date')
        else: # len(temp) is 0
            return ValueError(f'[ERROR] {date_time} not in calendar')


    def time_diff_market_days(self, start, end) -> int:
        start, end = self.dt_to_dfStr(start), self.dt_to_dfStr(end)
        temp = self.calendar[(self.calendar[DATE_TIME] > start) & (self.calendar[DATE_TIME] <= end)]
        return temp['is_market_day'].sum()

    def time_diff_calendar_days(self, start, end) -> int:
        start, end = self.dt_to_dfStr(start), self.dt_to_dfStr(end)
        return (end - start).days

    def generate_calender(self):
        self.calendar = pd.DataFrame()

        raw_data = pd.read_csv('data/hsi_hourly.csv')

        market_days = set(raw_data['date_time'].apply(lambda x: x[:10]))
        self.calendar[DATE_TIME] = pd.date_range(min(market_days), max(market_days))

        self.calendar['is_market_day'] = 0
        for i in self.calendar.index:
            if str(self.calendar.at[i, DATE_TIME])[:10] in market_days:
                self.calendar.at[i, 'is_market_day'] = 1

        self.calendar.to_csv('data/calendar.csv', index=False)

    @staticmethod
    def dt_to_dfStr(date_time) -> str:
        if type(date_time) == datetime:
            return datetime.strftime(date_time, '%Y-%m-%d %H:%M')
        elif type(date_time) == str:
            return date_time
        else:
            raise TypeError(f'[ERROR] variable {date_time} has unknown type to express date time')

if __name__ == '__main__':
    calendar_service = CalenderService()
    # calendar_service.generate_calender()
    print(calendar_service.calendar)