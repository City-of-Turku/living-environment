from django.conf import settings
from django.urls import include, re_path
from django.conf.urls.static import static

from living_environment.admin import admin_site
from living_environment.schemas import urls as doc_urls

urlpatterns = [
    re_path(r'^docs/', include(doc_urls), name='api-docs'),
    re_path(r'^admin/', admin_site.urls),
    re_path(r'^ckeditor5/', include('django_ckeditor_5.urls'), name="ck_editor_5_upload_file"),
    re_path(r'^', include('assignments.urls'), name='assignments'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        re_path(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
