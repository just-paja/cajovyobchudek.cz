from django.utils.translation import ugettext_lazy as _
from django.db.models import (
    model,
    DateTimeField,
    PositiveIntegerField,
    TextField,
    TimeField
)

PERIODS = (
    (1, _('Monday')),
    (2, _('Tuesday')),
    (3, _('Wednesday')),
    (4, _('Thursday')),
    (5, _('Friday')),
    (6, _('Saturday')),
    (7, _('Sunday')),
    (8, _('Weekend')),
    (9, _('Workweek')),
    (10, _('Public holiday')),
)


class BusinessHours(model):
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
        return _('Open on %(weekday)s from (%(from_hour)s - %(to_hour)s)' % {
            'weekday': self.weekday,
            'from_hour': self.from_hour,
            'to_hour': self.to_hour,
        })


class ClosingRules(models.Model):
    class Meta:
        verbose_name = _('Closing Rule')
        verbose_name_plural = _('Closing Rules')
        ordering = ['start']

    start = DateTimeField(_('Start'))
    end = DateTimeField(_('End'))
    reason = TextField(_('Reason'), null=True, blank=True)

    def __str__(self):
        return _('Closed from %(start)s to %(end)s' % {
            'start': self.start,
            'end': self.end
        })
