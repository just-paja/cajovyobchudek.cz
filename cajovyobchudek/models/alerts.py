from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from django.db.models import (
    DateTimeField,
    Q,
    CharField,
    Manager,
    Model,
    PositiveIntegerField,
    TextField
)

SEVERITY_INFO = 1
SEVERITY_WARNING = 2
SEVERITY_DANGER = 3

SEVERITY_CHOICES = (
    (SEVERITY_INFO, _('Informative')),
    (SEVERITY_WARNING, _('Warning')),
    (SEVERITY_DANGER, _('Danger')),
)

SEVERITY_MAP = {
    SEVERITY_INFO: 'info',
    SEVERITY_WARNING: 'warning',
    SEVERITY_DANGER: 'danger',
}


class AlertsManager(Manager):
    def get_active(self):
        now_dt = now()
        return self.filter(
            Q(publish_at__isnull=True) | Q(publish_at__lte=now_dt),
        ).filter(
            Q(hide_at__isnull=True) | Q(hide_at__gt=now_dt),
        )


class SiteAlert(Model):
    class Meta:
        verbose_name = _('Site Alert')
        verbose_name_plural = _('Site Alerts')

    name = CharField(max_length=31)
    severity = PositiveIntegerField(choices=SEVERITY_CHOICES, default=SEVERITY_INFO)
    text = TextField()
    publish_at = DateTimeField(null=True, blank=True)
    hide_at = DateTimeField(null=True, blank=True)
    objects = AlertsManager()

    @property
    def severity_class(self):
        return SEVERITY_MAP[self.severity]
