from django.db.models import Model
from django.utils.translation import gettext_lazy as _

from .fields import NameField


class Company(Model):
    class Meta:
        verbose_name = _('Company')
        verbose_name_plural = _('Companies')

    name = NameField(
        verbose_name=_('Company Name'),
        unique=True,
    )

    def __str__(self):
        return str(self.name)
