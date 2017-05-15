# -*- coding: utf-8 -*-
from django.contrib.admin import widgets
from sortedm2m.forms import SortedMultipleChoiceField


class SortedAsSelectedMultiple(widgets.FilteredSelectMultiple):
    def __init__(self, verbose_name, is_stacked, attrs=None, choices=()):
        super(SortedAsSelectedMultiple, self).__init__(verbose_name, is_stacked, attrs, choices)

    def optgroups(self, name, value, attrs=None):
        """
        Reorder selected options using ordering field from intermediate table.
        'Value' is a list of object database ids in order as specified by user.
        Result is reordered optgroups with selected options as specified in 'value', followed by unselected values.
        Optgroups is used for defining options of select widget in select.html template
        """
        groups = super(SortedAsSelectedMultiple, self).optgroups(name, value, attrs)
        reordered_groups = [list(groups[0])]
        unsorted = reordered_groups[0][1]
        selected = []
        unselected = []
        for data in unsorted:
            if data['selected']:
                selected.append(data)
            else:
                unselected.append(data)
        if selected:
            sorted_list = [''] * len(selected)
            for index, sel in enumerate(selected):
                list_index = value.index(str(sel['value']))
                sel['index'] = str(list_index)
                sorted_list[list_index] = sel
            for unsort in unselected:
                index += 1
                unsort['index'] = str(index)
                sorted_list.append(unsort)
            reordered_groups[0][1] = sorted_list
        return reordered_groups


class SortedAsSelectedMultipleChoiceField(SortedMultipleChoiceField):
    """
    Use select widget that preserves order of selected options
    """
    def __init__(self, queryset, required=True, label=None,
                 initial=None, help_text='', *args, **kwargs):
        widget = SortedAsSelectedMultiple(verbose_name=queryset.model._meta.verbose_name_plural,
                                          is_stacked=kwargs.get('is_stacked', False))
        super(SortedAsSelectedMultipleChoiceField, self).__init__(queryset, required, widget, label, initial,
                                                                  help_text=help_text, *args, **kwargs)
