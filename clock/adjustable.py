import datetime

from clock import DatetimeWrapper

try:
    from dateutil.relativedelta import relativedelta
except ImportError:
    raise RuntimeError('Adjustable clocks need dateutil package installed')


class CannotSetClockOffset(RuntimeError):
    pass


class BaseClock(DatetimeWrapper):
    def __init__(self, *, allow_adjustment=False):
        self.offset = datetime.timedelta(seconds=0)
        self.allow_adjustment = allow_adjustment

    def now(self):
        return super().now() + self.offset

    def reset(self):
        self.offset = datetime.timedelta(seconds=0)

    def adjust(self, *, days=0, hours=0, minutes=0, seconds=0):
        """
        Increase or decrease adjusted clock
        :param days: Integer days
        :param hours: Integer hours
        :param minutes: Integer minutes
        :param seconds: Integer seconds
        :return:
        """
        return self.set_offset(
            self.offset + datetime.timedelta(
                days=days,
                hours=hours, minutes=minutes, seconds=seconds
            )
        )

    def set_date(self, year=None, month=None, day=None):
        """
        Set the clock to a specific date

        :param year: Integer year
        :param month: Integer month
        :param day: Integer day
        :return: Current adjusted datetime
        """

        adjusted = self.now() + relativedelta(year=year, month=month, day=day)

        return self.set_offset(adjusted - datetime.datetime.now())

    def set_time(self, hour=None, minute=None, second=None):
        """
        Set the clock to a specific time

        :param hour: Integer hour
        :param minute: Integer minute
        :param second: Integer second
        :return: Current adjusted datetime
        """

        adjusted = self.now() + relativedelta(hour=hour, minute=minute, second=second)

        return self.set_offset(adjusted - datetime.datetime.now())

    def set_offset(self, offset: datetime.timedelta):
        if not self.allow_adjustment:
            raise CannotSetClockOffset()

        self.offset = offset

        return self.now()

    def save(self):
        raise NotImplementedError()


class LocalClock(BaseClock):
    def save(self):
        pass
