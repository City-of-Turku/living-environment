from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from assignments.views import AssignmentViewSet, SubmitAnswersViewSet, VoluntarySignupViewSet

router = DefaultRouter()
router.register(r'assignments', AssignmentViewSet, base_name='assignment')
router.register(r'signup', VoluntarySignupViewSet, base_name='signup')
api_urls = router.urls

urlpatterns = [
    url(r'^api/', include(api_urls)),
    url(r'^api/answers/(?P<slug>[-\w]+)/$', SubmitAnswersViewSet.as_view({'post': 'create', 'get': 'list'}),
        name='answers'),
]
