from django.urls import include, re_path
from rest_framework import permissions, renderers

from drf_yasg import openapi
from drf_yasg.views import get_schema_view





SchemaView = get_schema_view(
        info=openapi.Info(
            title='Living environment',
            default_version='v1',
            contact=openapi.Contact(email='sovellustuki@turku.fi'),
            license=openapi.License(name='MIT License')
        ),
        permission_classes=(permissions.IsAuthenticated, ),
    )


class SchemaJSView(SchemaView):
    renderer_classes = (renderers.SchemaJSRenderer, )

class SchemaDocsView(SchemaView):
    renderer_classes = (renderers.DocumentationRenderer, renderers.CoreJSONRenderer)



urls = [
    re_path(r'^$', SchemaDocsView.with_ui(), name='docs-index'),
    re_path(r'^schema.js$', SchemaJSView.with_ui(), name='schema-js')
]

