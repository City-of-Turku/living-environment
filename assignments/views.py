from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, ViewSet
from rest_framework_extensions.mixins import NestedViewSetMixin

from assignments.models import Assignment, Section
from assignments.serializers import AssignmentSerializer, SectionSerializer, SubmitAnswersSerializer


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

    def create(self, request, *args, **kwargs):
        answer = SubmitAnswersSerializer(data=request.data, context=self.get_serializer_context())
        answer.is_valid(raise_exception=True)
        answer.save()
        return Response(status=status.HTTP_201_CREATED)
