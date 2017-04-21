from django.conf.urls import include, url
from django.views.generic import TemplateView
from rest_framework_extensions.routers import ExtendedSimpleRouter

from assignments.views import AssignmentViewSet, SectionsViewSet

router = ExtendedSimpleRouter()
(
    router.register(r'assignments', AssignmentViewSet, base_name='assignment')
          .register(r'sections', SectionsViewSet, base_name='section', parents_query_lookups=['assignment__slug'])
)
api_urls = router.urls

urlpatterns = [
    url(r'^api/', include(api_urls))
]
