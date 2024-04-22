from django.urls import include, re_path
from rest_framework.routers import DefaultRouter

from assignments.views import AssignmentViewSet, ReportAssignmentViewSet, SubmitAnswersViewSet

router = DefaultRouter()
router.register(r'assignments', AssignmentViewSet, basename='assignment')
router.register(r'report', ReportAssignmentViewSet, basename='report')
router.register(r'answers/(?P<slug>[-\w]+)', SubmitAnswersViewSet, basename='answers')
api_urls = router.urls

urlpatterns = [
    re_path(r'^v1/', include(api_urls)),
]
