from django.contrib import admin
from django.shortcuts import reverse
from django.utils.html import format_html
from django.utils.translation import ugettext as _
from leaflet.admin import LeafletGeoAdmin
from polymorphic.admin import PolymorphicInlineSupportMixin, StackedPolymorphicInline

from assignments.forms import AssignmentForm
from assignments.models import (
    Assignment, BudgetingTarget, BudgetingTask, OpenTextTask, Section, Task, VoluntarySignupTask
)


@admin.register(BudgetingTarget)
class BudgetingTargetAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('name', 'unit_price', 'icon')
        }),
        (_('Additional data for budgeting text task'), {
            'classes': ('inner-group',),
            'fields': ('reference_amount', ('min_amount', 'max_amount'))
        })
    )


class TaskInline(StackedPolymorphicInline):
    class Media:
        """
        We are trying to remove section name from inline forms
        """
        css = {"all": ("css/assignment.css",)}

    class OpenTextInline(StackedPolymorphicInline.Child):
        extra = 0
        model = OpenTextTask

    class BudgetingTaskInline(StackedPolymorphicInline.Child):
        extra = 0
        model = BudgetingTask
        fieldsets = (
            (None, {
                'classes': ('inner-group',),
                'fields': ('order_number', 'name', 'budgeting_type')
            }),
            (_('Targets'), {
                'classes': ('inner-group',),
                'fields': ('targets',)
            }),
            (_('Units'), {
                'classes': ('inner-group',),
                'fields': ('unit', 'amount_of_consumption')
            }),
        )

    class VoluntarySignupTaskInline(StackedPolymorphicInline.Child):
        extra = 0
        model = VoluntarySignupTask

    model = Task
    child_inlines = (
        OpenTextInline,
        BudgetingTaskInline,
        VoluntarySignupTaskInline,
    )
    verbose_name = _('task')
    verbose_name_plural = _('tasks')


class SectionAdmin(PolymorphicInlineSupportMixin, admin.ModelAdmin):
    extra = 0
    view_on_site = False
    model = Section
    list_display = ('title', 'assignment', 'order_number',)
    list_editable = ('order_number',)
    list_filter = ('assignment',)
    inlines = (TaskInline,)
    fields = ('order_number', 'assignment', 'title', 'description', 'video')


class SectionInline(admin.TabularInline):
    """
    Inline sections for assignment record. We are trying here to simulate change_list page with editable order_number.
    """
    extra = 0
    view_on_site = False
    model = Section
    fields = ('edit_section', 'order_number',)
    readonly_fields = ('edit_section',)
    max_num = 0
    template = 'admin/assignments/assignment/sections.html'

    def has_delete_permission(self, request, obj=None):
        # Remove delete action
        return False

    def edit_section(self, obj):
        """
        link to edit section page
        """
        opts = obj._meta
        obj_url = reverse(
            'admin:%s_%s_change' % (opts.app_label, opts.model_name),
            args=(obj.id,),
            current_app=self.admin_site.name,
        )
        return format_html('<a href="{}">{}</a>'.format(obj_url, obj.title))
    edit_section.short_description = _('title')


@admin.register(Assignment)
class AssignmentAdmin(LeafletGeoAdmin):
    list_display = ['name', 'status', 'budget']
    list_filter = ('name', 'status')
    search_fields = ['name']
    actions_on_bottom = True
    actions_on_top = False
    prepopulated_fields = {
        'slug': ('name',)
    }
    inlines = (
        SectionInline,
    )
    form = AssignmentForm
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'status')
        }),
        (_('Area information'), {
            'classes': ('inner-group',),
            'fields': ('area', 'schools'),
        }),
        (_('Landing section'), {
            'classes': ('inner-group',),
            'fields': ('image', 'header', 'description'),
        }),
        (_('Budgeting'), {
            'classes': ('inner-group',),
            'fields': ('budget',),
        }),
    )

    class Media:
        """
        We are trying to remove section name from inline forms
        """
        css = {"all": ("css/assignment.css",)}

    def add_to_extra_context(self, extra_context):
        """
        Adding Section meta in order to create appropriate Add section link
        """
        extra_context = extra_context or {}
        extra_context['section_data'] = Section._meta
        return extra_context

    def change_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = self.add_to_extra_context(extra_context)
        return super(AssignmentAdmin, self).change_view(request, object_id, form_url, extra_context)

    def get_inline_instances(self, request, obj=None):
        """
        Remove section inline if we are adding new assignment
        as it is not possible to add new section until assignment is saved
        """
        orig_inline_instances = super(AssignmentAdmin, self).get_inline_instances(request, obj)
        inline_instances = []
        if obj is None:
            for inline in orig_inline_instances:
                if isinstance(inline, SectionInline):
                    continue
                inline_instances.append(inline)
        else:
            inline_instances = orig_inline_instances
        return inline_instances
