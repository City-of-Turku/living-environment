from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from assignments.views import AssignmentViewSet, SubmitAnswersViewSet

router = DefaultRouter()
router.register(r'assignments', AssignmentViewSet, base_name='assignment')
api_urls = router.urls

urlpatterns = [
    url(r'^api/', include(api_urls)),
    url(r'^api/answers/(?P<slug>[-\w]+)/$', SubmitAnswersViewSet.as_view({'post': 'create'}), name='answers'),
]
