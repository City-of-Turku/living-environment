from django.contrib import admin
from django.utils.translation import ugettext as _
from leaflet.admin import LeafletGeoAdmin
from nested_admin.nested import NestedModelAdminMixin, NestedTabularInline

from assignments.models import Assignment, BudgetingTarget, BudgetingTask, OpenTextTask, Section


class OpenTextInline(NestedTabularInline):
    extra = 0
    model = OpenTextTask


@admin.register(BudgetingTarget)
class BudgetingTargetAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('name', 'unit_price', 'reference_amount', 'icon')
        }),
        (_('Amount range'), {
            'fields': [('min_amount', 'max_amount')]
        })
    )


class BudgetingTaskInline(NestedTabularInline):
    extra = 0
    model = BudgetingTask


class SectionInline(NestedTabularInline):
    extra = 1
    inlines = [
        OpenTextInline, BudgetingTaskInline
    ]
    model = Section


@admin.register(Assignment)
class AssignmentAdmin(NestedModelAdminMixin, LeafletGeoAdmin):
    inlines = [
        SectionInline
    ]
    list_display = ['name', 'status', 'budget']
    list_filter = ('name', 'status')
    search_fields = ['name']
    actions_on_bottom = True
    actions_on_top = False
    prepopulated_fields = {
        'slug': ('name',)
    }
