from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet

from assignments.models import Assignment
from assignments.serializers import AssignmentSerializer, ReportAssignmentSerializer, SubmitAnswersSerializer


class AssignmentViewSet(ReadOnlyModelViewSet):
    """
    retrieve:

    Return the assignment

    - **Output JSON fields**:
        - *id*: assignment DB id
        - *name*: assignment name
        - *header*: assignment header
        - *description*: assignment description as html
        - *budget*: budget specified for the assignment
        - *slug*: unique assignment identifier used in assignment detail url
        - *status*: open/closed status of assignment
        - *area*: coordinates of assignment map area
        - *sections*: list of sections defined for assignment
            - *id*: section DB id
            - *title*: section title
            - *description*: section description as html
            - *video*: absolute url path to related video. If not defined, null is returned
            - *schools*: schools defined as participators in the assignment
                - *id*: school DB id
                - *name*: school name
                - *classes*: list of school classes in the specified school defined as participators in the assignment
                    - *id*: school class DB id
                    - *name*: school class name
            - *tasks*: list of tasks defined for section
                - *id*: task DB id
                - *order_number*: integer used for sorting tasks in section
                - *task_type*: type of the task [open_text_task/budgeting_task/voluntary_task]
                - *data*: task data, structure depends on task type:

                    1. *Open text task structure*:
                        - *question*: question asked

                    2. *Budgeting task structure*:
                        - *name*: name of budgeting task task
                        - *unit*: unit in which task amount is expressed [ha/pcs]
                        - *budgeting_type*: budgeting task type [text/map]
                        - *amount_of_consumption*: budgeting text tasks can have value specified that has to be
                        spent completely
                        - *targets*: budgeting targets related to the task
                            - *id*: target DB id
                            - *name*: target name
                            - *unit_price*: price of one target unit
                            - *reference_amount*: amount spent by public service that can be used as a reference value
                            for the student's answer
                            - *min_amount*: minimum amount used in answer validation
                            - *max_amount*: maximum amount used in answer validation, skip validation if amount is null
                            - *icon*: target icon [only for map targets]

                    3. *Voluntary task structure*:
                        - *name*: name of voluntary task

    list:

    Return a list of all opened assignments
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

    - **Input JSON fields**:
        - *school*: school DB id
        - *school_class*: school class DB id
        - *open_text_tasks*: list of open text task answers
            - *task*: open text task DB id this answer is related to
            - *answer*: submitted answer related to the task
        - *budgeting_targets*: list of budgeting target answers
            - *task*: budgeting task DB id this target answer is related to
            - *target*: budgeting target DB id this target answer is related to
            - *amount*: amount that has been set by user as an answer for this target
            - *point*: coordinates of the point placed by user on the map [only for map targets]
        - *voluntary_tasks*: list of voluntary task answers
            - *first_name*: volunteer's first name
            - *last_name*: volunteer's last name
            - *email*: volunteer's email
            - *phone*: volunteer's phone
            - *description*: in form of 'school name/class name'
            - *lat*: latitude of voluntary work point
            - *long*: longitude of voluntary work point
    - **Example**:

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
                    "first_name": "first",
                    "last_name": "last",
                    "email": "test@test.com",
                    "phone": "43423",
                    "description": "school/class",
                    "lat": 60.45148,
                    "long": 22.26869
                }]
            }
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

    Get all answers for specified assignment on report generation
    Answers can be additionally filtered by school and school class using query string

    - **Query string parameters**:
        - *school*: school DB id
        - *school_class*: school class DB id
    - **Example**:
        `https://www.example.com/api/report/<slug>/?school=1&&school_class=2`
    - **Output JSON fields**:
        - *name*: assignment name
        - *area*: coordinates of assignment map area
        - *sections*: list of assignment sections:
            - *title*: section title
            - *open_text_tasks*: list of open text tasks in section:
                - *question*: open text task question
                - *answers*: list of answers:
                    - *id*: answer DB id
                    - *task*: open text task DB id
                    - *answer*: submitted answer
            - *budgeting_tasks*: list of budgeting tasks in section:
                - *name*: name of budgeting task
                - *budgeting_type*: budgeting task type [text/map]
                - *answers*: list of budgeting target answers:
                    - *id*: answer DB id
                    - *amount*: budgeting target answer submitted amount
                    - *point*: budgeting target answer point placed [only for map targets]
                    - *target*: budgeting targets related to the answer
                        - *id*: target DB id
                        - *name*: target name
                        - *unit_price*: price of one target unit
                        - *reference_amount*: amount spent by public service
                        - *min_amount*: minimum amount set
                        - *max_amount*: maximum amount set
                        - *icon*: target icon [only for map targets]
            - *submissions*: Submissions statistics
                - *per_class*: list of submitted answers grouped by class
                    - *school_class__name*: school class name
                    - *count*: number of submitted answers
                - *per_school*: list of submitted answers grouped by school
                    - *school__name*: school name
                    - *count*: number of submitted answers
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
