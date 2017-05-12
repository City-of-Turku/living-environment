from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.viewsets import ReadOnlyModelViewSet

from assignments.models import Assignment
from assignments.serializers import AssignmentSerializer, ReportAssignmentSerializer, SubmitAnswersSerializer


class AssignmentViewSet(ReadOnlyModelViewSet):
    """
    retrieve:
    Return the given assignment.

    list:
    Return a list of all the existing assignments.
    """

    serializer_class = AssignmentSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        """
        Get only opened assignments
        """
        return Assignment.objects.filter(status=Assignment.STATUS_OPEN)


class SubmitAnswersViewSet(CreateModelMixin, GenericViewSet):
    """
    Submit assignment answers

    - **Purpose**: Submit answers for specified assignment.
    - **Example of input json**
        ```
        {
            "school": 1,
            "school_class": 1,
            "open_text_tasks": [
            {
                "task": 2,
                "answer": "My first answer"
            }],
            "budgeting_targets": [{
                "task": 1,
                "target": 1,
                "amount": 200,
                "point": [123.343, 444.1232]
                }
            ],
            "voluntary_tasks": [{
                "first_name": "",
                "last_name": "last",
                "email": "test@test.com",
                "phone": "43423",
                "description": "school/class",
                "lat": 60.45148,
                "long": 22.26869
            }]
        }
        ```
    """
    serializer_class = SubmitAnswersSerializer

    def get_serializer_context(self):
        context = super(SubmitAnswersViewSet, self).get_serializer_context()
        if 'slug' in self.kwargs:
            # if not api documentation
            context['assignment_slug'] = self.kwargs['slug']
        return context


class ReportAssignmentViewSet(RetrieveModelMixin, GenericViewSet):
    """
    Get answers

    - **Purpose**: Get all answers for specified assignment on report generation.
    Answers can be additionally filtered by school and school class using GET query
    params
    - **GET query params**:
        - *school*: school id
        - *school_class*: school class id
    - **Example usage**:
        `https://www.example.com/api/report/<slug>/?school=1&&school_class=2`
    """
    serializer_class = ReportAssignmentSerializer

    queryset = Assignment.objects.all()
    lookup_field = 'slug'

    def get_serializer_context(self):
        context = super(ReportAssignmentViewSet, self).get_serializer_context()
        task_query_params = {
            'school': self.request.query_params.get('school', None),
            'school_class': self.request.query_params.get('school_class', None)
        }
        context.update({
            'query_params': task_query_params
        })
        return context
