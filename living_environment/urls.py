from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static

from living_environment.admin import admin_site

urlpatterns = [
    url(r'^admin/', admin_site.urls),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^nested_admin/', include('nested_admin.urls')),
    url(r'^', include('assignments.urls', namespace='assignments')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
