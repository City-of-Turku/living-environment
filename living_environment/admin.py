from django.contrib.admin import AdminSite
from django.contrib.auth.models import Group, User
from django.utils.translation import gettext_lazy as _

from assignments.admin import AssignmentAdmin, BudgetingTargetAdmin, SectionAdmin
from assignments.models import Assignment, BudgetingTarget, School, SchoolClass, Section


class TurunAdminSite(AdminSite):
    site_title = _('Living environment - Admin')
    site_header = _('Turun Kaupunki')
    index_title = _('Site administration')
    site_url = None


admin_site = TurunAdminSite()
admin_site.register(Assignment, AssignmentAdmin)
admin_site.register(Section, SectionAdmin)
admin_site.register(BudgetingTarget, BudgetingTargetAdmin)
admin_site.register(School)
admin_site.register(SchoolClass)
admin_site.register(User)
admin_site.register(Group)
