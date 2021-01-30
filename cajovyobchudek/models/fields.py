from django.db.models import BooleanField, CASCADE, CharField, ForeignKey
from django.utils.translation import gettext_lazy as _

from markdownfield.models import MarkdownField, RenderedMarkdownField
from markdownfield.validators import VALIDATOR_STANDARD


class NameField(CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = kwargs.get('max_length', 63)
        kwargs['verbose_name'] = kwargs.get('verbose_name', _('Name'))
        super().__init__(*args, **kwargs)


class DescriptionField(MarkdownField):
    def __init__(self, *args, **kwargs):
        kwargs['blank'] = kwargs.get('blank', True)
        kwargs['null'] = kwargs.get('null', True)
        kwargs['validator'] = kwargs.get('validator', VALIDATOR_STANDARD)
        kwargs['verbose_name'] = kwargs.get('verbose_name', _('Description'))
        super().__init__(*args, **kwargs)


class FaculativeForeignKey(ForeignKey):
    def __init__(self, *args, **kwargs):
        kwargs['blank'] = kwargs.get('blank', True)
        kwargs['null'] = kwargs.get('null', True)
        kwargs['on_delete'] = kwargs.get('on_delete', CASCADE)
        super().__init__(*args, **kwargs)


class RenderedDescriptionField(RenderedMarkdownField):
    def __init__(self, *args, **kwargs):
        kwargs['blank'] = kwargs.get('blank', True)
        kwargs['null'] = kwargs.get('null', True)
        super().__init__(*args, **kwargs)


class VisibilityField(BooleanField):
    def __init__(self, *args, **kwargs):
        kwargs['default'] = kwargs.get('default', True)
        kwargs['verbose_name'] = kwargs.get('verbose_name', _('Public'))
        super().__init__(*args, **kwargs)
