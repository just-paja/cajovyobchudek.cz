from datetime import date, datetime, timedelta
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import make_aware
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

PERIODS = (
    (8, _('Work days')),
    (9, _('Public holiday')),
)

def get_weekday_date(today, weekday):
    current_weekday = today.isoweekday()
    distance = current_weekday - weekday
    if current_weekday > weekday:
        distance = distance - 7
    return today - timedelta(days=distance)


class WeekDay:
    @classmethod
    def all(cls):
        items = {}
        today = date.today()
        for weekday, name in WEEKDAYS:
            items[weekday] = cls(
                weekday,
                name,
                get_weekday_date(today, weekday)
            )
        return items

    def __init__(self, weekday, name, day_date=None):
        self.weekday = weekday
        self.name = name
        self.hour_blocks = []
        self.date = day_date

    def add_hours(self, block):
        self.hour_blocks.append(block)

    @property
    def empty(self):
        return len(self.hour_blocks) == 0

    @property
    def blocks(self):
        blocks = []
        for block in self.hour_blocks:
            blocks.append({
                'end': make_aware(datetime.combine(self.date, block.to_hour)),
                'from_hour': block.from_hour,
                'start': make_aware(datetime.combine(self.date, block.from_hour)),
                'to_hour': block.to_hour,
            })
        return blocks

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
        hours = cls.objects.all()
        weekdays = WeekDay.all()
        for block in hours:
            weekdays[block.weekday].add_hours(block)
        return weekdays


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
