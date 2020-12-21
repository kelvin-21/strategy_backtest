from datetime import datetime, timedelta
import logging


class Timer():
    def __init__(self):
        self.time_points = []

    def initialize(self):
        self.time_points = []

    def time(self, msg=''):
        if not self.time_points:
            self.initialize()
            self.time_points.append(datetime.now())
            time_point = 'Start time: {}'.format(self.dt_to_dtStr(self.time_points[0]))
            logging.info(f'[TIMER] {time_point}, {msg}')
        else:
            self.time_points.append(datetime.now())
            time_point = 'Start time: {}'.format(self.dt_to_dtStr(self.time_points[0]))
            time_diff = 'this step time = {}'.format(self.time_diff(self.time_points[-2], self.time_points[-1]))
            time_total = 'total time = {}'.format(self.time_diff(self.time_points[0], self.time_points[-1]))
            logging.info(f'[TIMER] {time_point}, {time_diff}, {time_total}, {msg}')

    @staticmethod
    def dt_to_dtStr(date_time_obj: datetime) -> str:
        return date_time_obj.strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def time_diff(start: datetime, end: datetime) -> str:
        diff_seconds = (end - start).seconds
        minute = int(diff_seconds / 60)
        second = diff_seconds % 60
        if minute == 0:
            return '{} sec'.format(second)
        else:
            return '{} min {} sec'.format(minute, second)

if __name__ == '__main__':
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    t1 = datetime(2020, 12, 17, 21, 18, 50)
    t2 = datetime(2020, 12, 17, 21, 20, 30)
    diff = t1 - t2
    print(f'{t1} {t2}')