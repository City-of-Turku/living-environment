from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework_extensions.mixins import NestedViewSetMixin

from assignments.models import Assignment, Section
from assignments.serializers import AssignmentSerializer, SectionSerializer


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
