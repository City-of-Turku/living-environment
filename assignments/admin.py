from django.contrib import admin
from django.utils.translation import ugettext as _
from leaflet.admin import LeafletGeoAdmin
from nested_admin.nested import NestedModelAdminMixin, NestedStackedInline

from assignments.models import Assignment, BudgetingTarget, BudgetingTask, OpenTextTask, School, SchoolClass, Section


class OpenTextInline(NestedStackedInline):
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


class BudgetingTaskInline(NestedStackedInline):
    extra = 0
    model = BudgetingTask


class SectionInline(NestedStackedInline):
    class Media:
        js = ("admin/ckeditor-nested-inline-fix.js",)

    extra = 1
    inlines = [
        OpenTextInline, BudgetingTaskInline
    ]
    model = Section


class SchoolInline(NestedStackedInline):
    extra = 1
    model = School


@admin.register(Assignment)
class AssignmentAdmin(NestedModelAdminMixin, LeafletGeoAdmin):
    inlines = [
        SchoolInline,
        SectionInline,
    ]
    list_display = ['name', 'header', 'status', 'budget']
    list_filter = ('name', 'status')
    search_fields = ['name']
    actions_on_bottom = True
    actions_on_top = False
    prepopulated_fields = {
        'slug': ('name',)
    }


@admin.register(SchoolClass)
class SchoolClassAdmin(admin.ModelAdmin):
    fields = ['name']
