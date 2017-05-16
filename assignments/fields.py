# -*- coding: utf-8 -*-
from sortedm2m.fields import SortedManyToManyField

from assignments.forms import SortedAsSelectedMultipleChoiceField


class SortedAsSelectedManyToManyField(SortedManyToManyField):
    def formfield(self, **kwargs):
        defaults = {}
        if self.sorted:
            defaults['form_class'] = SortedAsSelectedMultipleChoiceField
        defaults.update(kwargs)
        return super(SortedAsSelectedManyToManyField, self).formfield(**defaults)
