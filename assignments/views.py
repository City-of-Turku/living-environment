from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet, ViewSet
from rest_framework_extensions.mixins import NestedViewSetMixin

from assignments.models import Assignment, Section
from assignments.serializers import (
    AssignmentSerializer, ReportAssignmentSerializer, SectionSerializer, SubmitAnswersSerializer,
    VoluntarySignupSerializer
)


class AssignmentViewSet(ReadOnlyModelViewSet):
    serializer_class = AssignmentSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        """
        Get only opened assignments
        """
        return Assignment.objects.filter(status=Assignment.STATUS_OPEN)


class SectionsViewSet(NestedViewSetMixin, ReadOnlyModelViewSet):
    serializer_class = SectionSerializer
    queryset = Section.objects.filter(assignment__status=Assignment.STATUS_OPEN)


class SubmitAnswersViewSet(ViewSet):

    def get_serializer_context(self):
        context = {
            'assignment_slug': self.kwargs['slug']
        }
        return context

    def get_report_context(self):
        context = self.get_serializer_context()
        task_query_params = {
            'school': self.request.query_params.get('school', None),
            'school_class': self.request.query_params.get('school_class', None)
        }
        context.update({
            'query_params': task_query_params
        })
        return context

    def create(self, request, *args, **kwargs):
        answer = SubmitAnswersSerializer(data=request.data, context=self.get_serializer_context())
        answer.is_valid(raise_exception=True)
        answer.save()
        return Response(status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        assignment = get_object_or_404(Assignment, slug=kwargs['slug'])
        serializer = ReportAssignmentSerializer(assignment, context=self.get_report_context())
        return Response(serializer.data)


class VoluntarySignupViewSet(CreateModelMixin, GenericViewSet):
    serializer_class = VoluntarySignupSerializer
