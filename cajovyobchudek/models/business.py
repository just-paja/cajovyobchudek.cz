from datetime import date, datetime, timedelta
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import make_aware, now
from django.db.models import (
    Model,
    DateTimeField,
    PositiveIntegerField,
    TextField,
    TimeField
)

import holidays

DAY_MONDAY = 1
DAY_TUESDAY = 2
DAY_WEDNESDAY = 3
DAY_THURSDAY = 4
DAY_FRIDAY = 5
DAY_SATURDAY = 6
DAY_SUNDAY = 7

WEEKDAYS = (
    (DAY_MONDAY, _('Monday')),
    (DAY_TUESDAY, _('Tuesday')),
    (DAY_WEDNESDAY, _('Wednesday')),
    (DAY_THURSDAY, _('Thursday')),
    (DAY_FRIDAY, _('Friday')),
    (DAY_SATURDAY, _('Saturday')),
    (DAY_SUNDAY, _('Sunday')),
)

WORK_DAYS = [
    DAY_MONDAY,
    DAY_TUESDAY,
    DAY_WEDNESDAY,
    DAY_THURSDAY,
    DAY_FRIDAY
]

PERIOD_WORK_DAYS = 8
PERIOD_PUBLIC_HOLIDAY = 9

PERIODS = WEEKDAYS + (
    (PERIOD_WORK_DAYS, _('Work days')),
    (PERIOD_PUBLIC_HOLIDAY, _('Public holiday')),
)


def get_weekday_date(today, weekday):
    current_weekday = today.isoweekday()
    distance = current_weekday - weekday
    if current_weekday > weekday:
        distance = distance - 7
    return today - timedelta(days=distance)


def get_block_start(block):
    return block['start']


def add_block_to_work_days(weekdays, block):
    for tup in weekdays.items():
        print(tup[1], tup[1].work_day)
        if tup[1].work_day:
            tup[1].add_hours(block)


def add_block_to_public_holiday(weekdays, block):
    for tup in weekdays.items():
        if tup[1].holiday:
            tup[1].add_hours(block)


class WeekDay:
    holidays = holidays.Czechia()

    @classmethod
    def all(cls, closing_hours):
        items = {}
        today = date.today()
        for weekday, name in WEEKDAYS:
            items[weekday] = cls(
                weekday,
                name,
                get_weekday_date(today, weekday),
                closing_hours
            )
        return items

    def __init__(self, weekday, name, day_date=None, closing_hours=None):
        self.weekday = weekday
        self.name = name
        self.blocks = []
        self.closing_hours = closing_hours if closing_hours else []
        self.date = day_date
        self.closed_for_reason = None

    def get_closing_rule(self, block):
        for closed in self.closing_hours:
            if (
                closed.start <= block['start'] <= closed.end or
                closed.start <= block['end'] <= closed.end
            ):
                return closed
        return None

    def add_hours(self, block):
        datetime_now = now()
        end = make_aware(datetime.combine(self.date, block.to_hour))
        start = make_aware(datetime.combine(self.date, block.from_hour))
        is_active = start <= datetime_now <= end
        block = {
            'end': end,
            'from_hour': block.from_hour,
            'start': start,
            'to_hour': block.to_hour,
            'is_active': is_active,
        }
        closing_rule = self.get_closing_rule(block)
        if closing_rule:
            self.closed_for_reason = closing_rule.reason
        else:
            self.blocks.append(block)
            self.blocks.sort(key=get_block_start)

    @property
    def empty(self):
        return len(self.blocks) == 0

    @property
    def closed_for(self):
        if self.closed_for_reason:
            return self.closed_for_reason
        if self.holiday:
            return self.holidays.get(self.date)
        return None

    @property
    def today(self):
        return self.date == date.today()

    @property
    def work_day(self):
        return self.weekday in WORK_DAYS

    @property
    def holiday(self):
        return self.date in self.holidays


class BusinessHours(Model):
    class Meta:
        verbose_name = _('Business Hours')
        verbose_name_plural = _('Business Hours')
        ordering = ['weekday', 'from_hour']

    weekday = PositiveIntegerField(
        verbose_name=_('Weekday'),
        choices=PERIODS,
    )
    from_hour = TimeField(_('Opening'))
    to_hour = TimeField(_('Closing'))

    def __str__(self):
        return str(_('Open on %(weekday)s from (%(from_hour)s - %(to_hour)s)' % {
            'weekday': self.weekday,
            'from_hour': self.from_hour,
            'to_hour': self.to_hour,
        }))

    @classmethod
    def get_weekdays(cls):
        closing_hours = ClosingRules.objects.filter(end__gt=now() - timedelta(days=7))
        hours = cls.objects.all()
        weekdays = WeekDay.all(closing_hours)
        for block in hours:
            if block.weekday == PERIOD_WORK_DAYS:
                add_block_to_work_days(weekdays, block)
            elif block.weekday == PERIOD_PUBLIC_HOLIDAY:
                add_block_to_public_holiday(weekdays, block)
            elif not weekdays[block.weekday].holiday:
                weekdays[block.weekday].add_hours(block)
        return weekdays

    @staticmethod
    def get_active_business_block(weekdays_blocks):
        try:
            return next(block for block in weekdays_blocks if block['is_active'])
        except StopIteration:
            return None

    @staticmethod
    def get_next_business_block(weekdays_blocks):
        now_datetime = now()
        next_block = None
        for block in weekdays_blocks:
            if now_datetime < block['start']:
                next_block = block
                break
        try:
            return next_block if next_block else weekdays_blocks[0]
        except IndexError:
            return None

    @staticmethod
    def get_weekdays_blocks(weekdays):
        blocks = []
        for day in weekdays.items():
            blocks = blocks + day[1].blocks
        blocks.sort(key=get_block_start)
        return blocks

    @classmethod
    def get_closing_datetime(cls, weekdays_blocks):
        block = cls.get_active_business_block(weekdays_blocks)
        return block['end'] if block else None

    @classmethod
    def get_opening_datetime(cls, weekdays_blocks):
        block = cls.get_next_business_block(weekdays_blocks)
        return block['start'] if block else None


class ClosingRules(Model):
    class Meta:
        verbose_name = _('Closing Rule')
        verbose_name_plural = _('Closing Rules')
        ordering = ['start']

    start = DateTimeField(_('Start'))
    end = DateTimeField(_('End'))
    reason = TextField(_('Reason'), null=True, blank=True)

    def __str__(self):
        return str(_('Closed from %(start)s to %(end)s' % {
            'start': self.start,
            'end': self.end
        }))
