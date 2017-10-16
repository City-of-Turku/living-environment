import sys

from django.conf import settings
from django.db.models import Count
from rest_framework import serializers

from assignments.helper import post_to_feedback_system
from assignments.models import (
    Assignment, BudgetingTarget, BudgetingTargetAnswer, BudgetingTask, OpenTextAnswer, OpenTextTask, School,
    SchoolClass, Section, Submission, Task, VoluntarySignupTask
)

SERIALIZERS_MODULE = sys.modules[__name__]


class OpenTextTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpenTextTask
        fields = ['question']


class BudgetingTargetSerializer(serializers.ModelSerializer):

    class Meta:
        model = BudgetingTarget
        fields = ['id', 'name', 'unit_price', 'reference_amount',
                  'min_amount', 'max_amount', 'icon']


class BudgetingTaskSerializer(serializers.ModelSerializer):
    targets = BudgetingTargetSerializer(many=True)
    unit = serializers.SerializerMethodField()

    class Meta:
        model = BudgetingTask
        fields = ['name', 'unit', 'budgeting_type', 'targets', 'amount_of_consumption']
        read_only_fields = ('name', 'unit', 'amount_of_consumption')

    def get_unit(self, obj):
        return obj.get_unit_display()


class VoluntarySignupTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoluntarySignupTask
        fields = ['name']


class TaskSerializer(serializers.ModelSerializer):
    data = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ['id', 'order_number', 'task_type', 'data']

    def get_data(self, obj):
        """
        Serialized data depend on Task type.
        Serializer classes should be named as '<model name>Serializer'. If Serializer class is missing,
        return empty data
        """
        try:
            serializer_type = getattr(SERIALIZERS_MODULE, '{}Serializer'.format(obj.__class__.__name__))
        except AttributeError:
            return ''
        serializer = serializer_type(obj)
        return serializer.data


class SectionSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True)

    class Meta:
        model = Section
        fields = ['id', 'title', 'description', 'video', 'tasks']


class SchoolClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolClass
        fields = ['id', 'name']


class SchoolSerializer(serializers.ModelSerializer):
    classes = SchoolClassSerializer(many=True)

    class Meta:
        model = School
        fields = ['id', 'name', 'classes']


class AssignmentSerializer(serializers.ModelSerializer):
    schools = SchoolSerializer(many=True)
    sections = SectionSerializer(many=True)

    class Meta:
        model = Assignment
        fields = ['id', 'name', 'header', 'description',
                  'budget', 'image', 'slug', 'status',
                  'area', 'sections', 'schools']


class OpenTextAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpenTextAnswer
        fields = ['id', 'task', 'answer']


class BudgetingTargetAnswerSerializer(serializers.ModelSerializer):
    point = serializers.JSONField(required=False, allow_null=True)

    class Meta:
        model = BudgetingTargetAnswer
        fields = ['id', 'task', 'target', 'amount', 'point']

    def validate_point(self, data):
        if not data:
            return None
        if type(data) is not list:
            raise serializers.ValidationError('Invalid point format. You have to specify list')
        get_json_data = {
            'type': 'Point',
            'coordinates': data
        }
        return get_json_data


class VoluntarySignupSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    email = serializers.EmailField(allow_blank=True)
    phone = serializers.CharField(max_length=255, allow_blank=True)
    description = serializers.CharField(max_length=512)
    lat = serializers.DecimalField(max_digits=None, decimal_places=None, min_value=-90, max_value=90)
    long = serializers.DecimalField(max_digits=None, decimal_places=None, min_value=-180, max_value=180)

    def to_internal_value(self, data):
        validated_data = super(VoluntarySignupSerializer, self).to_internal_value(data)
        validated_data['service_code'] = settings.FEEDBACK_SERVICE_CODE
        return validated_data


class SubmitAnswersSerializer(serializers.Serializer):
    school = serializers.PrimaryKeyRelatedField(queryset=School.objects.all(),
                                                help_text='school DB id')
    school_class = serializers.PrimaryKeyRelatedField(queryset=SchoolClass.objects.all(),
                                                      help_text='school class DB id')
    open_text_tasks = OpenTextAnswerSerializer(many=True, required=False, allow_null=True,
                                               help_text='list of open text task answers')
    budgeting_targets = BudgetingTargetAnswerSerializer(many=True, required=False, allow_null=True,
                                                        help_text='list of budgeting target answers')
    voluntary_tasks = VoluntarySignupSerializer(many=True, required=False, allow_null=True,
                                                help_text='voluntary task answers')

    def validate_school(self, value):
        if not value.assignments.filter(slug=self.context['assignment_slug']).exists():
            raise serializers.ValidationError('You specified school on wrong assignment')
        return value

    def validate(self, data):
        if not data['school_class'].schools.filter(id__in=[data['school'].id]).exists():
            raise serializers.ValidationError({'school_class': 'Specified class does not exist in specified school'})
        return data

    def save(self):
        submission_instance = Submission.objects.create(school=self.validated_data['school'],
                                                        school_class=self.validated_data['school_class'])
        open_text_answers = [OpenTextAnswer(
            submission=submission_instance,
            **open_text_data) for open_text_data in self.validated_data.get('open_text_tasks', [])]
        OpenTextAnswer.objects.bulk_create(open_text_answers)
        budgeting_target_answers = [BudgetingTargetAnswer(
            submission=submission_instance,
            **budgeting_text_data) for budgeting_text_data in self.validated_data.get('budgeting_targets', [])]
        BudgetingTargetAnswer.objects.bulk_create(budgeting_target_answers)
        for voluntary_data in self.validated_data.get('voluntary_tasks', []):
            post_to_feedback_system(settings.FEEDBACK_SYSTEM_URL, voluntary_data, api_key=settings.FEEDBACK_API_KEY)


# serializers used for getting answers for report generation
class ReportOpenTextTaskSerializer(serializers.ModelSerializer):
    answers = serializers.SerializerMethodField()

    class Meta:
        model = OpenTextTask
        fields = ['question', 'answers']

    def get_answers(self, obj):
        answers = obj.get_answers(**self.context['query_params'])
        serializer = OpenTextAnswerSerializer(instance=answers, many=True)
        return serializer.data


class ReportBudgetingTargetSerializer(serializers.ModelSerializer):
    target = BudgetingTargetSerializer()

    class Meta:
        model = BudgetingTargetAnswer
        fields = ['id', 'amount', 'point', 'target']


class ReportBudgetingTaskSerializer(serializers.ModelSerializer):
    answers = serializers.SerializerMethodField()

    class Meta:
        model = BudgetingTask
        fields = ['name', 'budgeting_type', 'answers']

    def get_answers(self, obj):
        answers = obj.get_answers(**self.context['query_params'])
        serializer = ReportBudgetingTargetSerializer(instance=answers, many=True)
        return serializer.data


class ReportSectionSerializer(serializers.ModelSerializer):
    open_text_tasks = serializers.SerializerMethodField()
    budgeting_tasks = serializers.SerializerMethodField()

    class Meta:
        model = Section
        fields = ['title', 'open_text_tasks', 'budgeting_tasks']

    def get_open_text_tasks(self, obj):
        open_text_tasks = obj.tasks.instance_of(OpenTextTask)
        serializer = ReportOpenTextTaskSerializer(open_text_tasks, many=True, context=self.context)
        return serializer.data

    def get_budgeting_tasks(self, obj):
        budgeting_tasks = obj.tasks.instance_of(BudgetingTask)
        serializer = ReportBudgetingTaskSerializer(budgeting_tasks, many=True, context=self.context)
        return serializer.data


class ReportAssignmentSerializer(serializers.ModelSerializer):
    submissions = serializers.SerializerMethodField()
    sections = ReportSectionSerializer(many=True)

    class Meta:
        model = Assignment
        fields = ['name', 'area', 'sections', 'submissions']

    def get_submissions(self, obj):
        submissions = obj.get_submissions(**self.context['query_params'])
        submissions_per_school = submissions.values('school__name').annotate(count=Count('id')).order_by('school__name')
        submissions_per_class = submissions.values('school_class__name').annotate(count=Count('id')).order_by(
            'school_class__name')
        return {
            'per_school': submissions_per_school,
            'per_class': submissions_per_class
        }
