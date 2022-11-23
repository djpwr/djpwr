import datetime


class DatetimeWrapper:
    def now(self):
        return datetime.datetime.now()

    def time(self):
        return self.now().time()

    def today(self):
        return self.now().date()
