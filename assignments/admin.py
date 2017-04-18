from django.contrib import admin
from assignments.models import Assignment, Section, OpenTextTask
from nested_admin.nested import NestedModelAdminMixin, NestedStackedInline, NestedTabularInline
from leaflet.admin import LeafletGeoAdmin


class OpenTextInline(NestedTabularInline):
    extra = 1
    model = OpenTextTask


class SectionInline(NestedTabularInline):
    extra = 1
    inlines = [
        OpenTextInline
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





