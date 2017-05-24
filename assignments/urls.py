from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from assignments.views import AssignmentViewSet, ReportAssignmentViewSet, SubmitAnswersViewSet

router = DefaultRouter()
router.register(r'assignments', AssignmentViewSet, base_name='assignment')
router.register(r'report', ReportAssignmentViewSet, base_name='report')
router.register(r'answers/(?P<slug>[-\w]+)', SubmitAnswersViewSet, base_name='answers')
api_urls = router.urls

urlpatterns = [
    url(r'^api/', include(api_urls)),
]
