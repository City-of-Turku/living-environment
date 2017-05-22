from django import http
from django.conf.urls import include, url
from rest_framework.compat import is_authenticated
from rest_framework.renderers import CoreJSONRenderer, DocumentationRenderer, SchemaJSRenderer
from rest_framework.schemas import SchemaGenerator, SchemaView


class AuthorizedSchemaView(SchemaView):
    """
    Customized SchemaView that checks if user is authenticated and returns 403 Forbidden otherwise
    """

    def get(self, request, *args, **kwargs):
        if request.user and is_authenticated(request.user):
            return super(AuthorizedSchemaView, self).get(request, *args, **kwargs)
        return http.HttpResponseForbidden('<h1>403 Forbidden</h1>', content_type='text/html')


def get_schema_view(title=None, url=None, description=None, urlconf=None, renderer_classes=None, public=False):
    """
    Return a schema view.
    """
    generator = SchemaGenerator(title=title, url=url, description=description, urlconf=urlconf)
    return AuthorizedSchemaView.as_view(
        renderer_classes=renderer_classes,
        schema_generator=generator,
        public=public,
    )


def get_docs_view(title=None, description=None, schema_url=None, public=True):
    renderer_classes = [DocumentationRenderer, CoreJSONRenderer]

    return get_schema_view(
        title=title,
        url=schema_url,
        description=description,
        renderer_classes=renderer_classes,
        public=public
    )


def get_schemajs_view(title=None, description=None, schema_url=None, public=True):
    renderer_classes = [SchemaJSRenderer]

    return get_schema_view(
        title=title,
        url=schema_url,
        description=description,
        renderer_classes=renderer_classes,
        public=public
    )


def include_docs_urls(title=None, description=None, schema_url=None, public=True):
    docs_view = get_docs_view(
        title=title,
        description=description,
        schema_url=schema_url,
        public=public
    )
    schema_js_view = get_schemajs_view(
        title=title,
        description=description,
        schema_url=schema_url,
        public=public
    )
    urls = [
        url(r'^$', docs_view, name='docs-index'),
        url(r'^schema.js$', schema_js_view, name='schema-js')
    ]
    return include(urls, namespace='api-docs')
