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

WEEKDAYS = (
    (1, _('Monday')),
    (2, _('Tuesday')),
    (3, _('Wednesday')),
    (4, _('Thursday')),
    (5, _('Friday')),
    (6, _('Saturday')),
    (7, _('Sunday')),
)

PERIODS = WEEKDAYS + (
    (8, _('Work days')),
    (9, _('Public holiday')),
)


def get_weekday_date(today, weekday):
    current_weekday = today.isoweekday()
    distance = current_weekday - weekday
    if current_weekday > weekday:
        distance = distance - 7
    return today - timedelta(days=distance)


def get_block_start(block):
    return block['start']


class WeekDay:
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
        self.closed_for = None

    def get_closing_rule(self, block):
        for closed in self.closing_hours:
            if (
                closed.start <= block['start'] <= closed.end or
                closed.start <= block['end'] <= closed.end
            ):
                print("A: <%s, %s>" % (closed.start, closed.end))
                print("B: <%s, %s>" % (block['start'], block['end']))
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
            self.closed_for = closing_rule.reason
        else:
            self.blocks.append(block)

    @property
    def empty(self):
        return len(self.blocks) == 0

    @property
    def today(self):
        return self.date == date.today()


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
