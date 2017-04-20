from rest_framework import serializers

from assignments.models import (
    Assignment, BudgetingTarget, BudgetingTargetAnswer, BudgetingTask, OpenTextAnswer, OpenTextTask, Section, School,
    SchoolClass, Student
)


class OpenTextTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpenTextTask
        fields = ['id', 'question']


class BudgetingTargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = BudgetingTarget
        fields = ['id', 'name', 'unit_price', 'reference_amount', 'min_amount', 'max_amount', 'icon']


class BudgetingTaskSerializer(serializers.ModelSerializer):
    targets = BudgetingTargetSerializer(many=True)
    unit = serializers.SerializerMethodField()

    class Meta:
        model = BudgetingTask
        fields = ['id', 'name', 'unit', 'targets', 'amount_of_consumption']
        read_only_fields = ('name', 'unit', 'amount_of_consumption')

    def get_unit(self, obj):
        return obj.get_unit_display()


class SectionSerializer(serializers.ModelSerializer):
    open_text_tasks = OpenTextTaskSerializer(many=True, source='opentexttasks')
    budgeting_tasks = BudgetingTaskSerializer(many=True, source='budgetingtasks')

    class Meta:
        model = Section
        fields = ['id', 'title', 'description', 'video', 'open_text_tasks', 'budgeting_tasks']


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
        fields = ['id', 'name', 'budget', 'slug', 'status', 'area', 'sections', 'schools']


class OpenTextAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpenTextAnswer
        fields = ['task', 'answer']


class BudgetingTargetAnswerSerializer(serializers.ModelSerializer):
    point = serializers.JSONField(required=False, allow_null=True)

    class Meta:
        model = BudgetingTargetAnswer
        fields = ['task', 'target', 'amount', 'point']

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


class SubmitAnswersSerializer(serializers.Serializer):
    school = serializers.PrimaryKeyRelatedField(queryset=School.objects.all())
    school_class = serializers.PrimaryKeyRelatedField(queryset=SchoolClass.objects.all())
    open_text_tasks = OpenTextAnswerSerializer(many=True)
    budgeting_targets = BudgetingTargetAnswerSerializer(many=True)

    def validate_school(self, value):
        if value.assignment.slug != self.context['assignment_slug']:
            raise serializers.ValidationError('You specified school on wrong assignment')
        return value

    def validate(self, data):
        if not data['school_class'].schools.filter(id__in=[data['school'].id]).exists():
            raise serializers.ValidationError({'school_class': 'Specified class does not exist in specified school'})
        return data

    def save(self):
        student_instance = Student.objects.create(school=self.validated_data['school'],
                                                  school_class=self.validated_data['school_class'])
        open_text_answers = [OpenTextAnswer(
            student=student_instance, **open_text_data) for open_text_data in self.validated_data['open_text_tasks']]
        OpenTextAnswer.objects.bulk_create(open_text_answers)
        budgeting_target_answers = [BudgetingTargetAnswer(
            student=student_instance,
            **budgeting_text_data) for budgeting_text_data in self.validated_data['budgeting_targets']]
        BudgetingTargetAnswer.objects.bulk_create(budgeting_target_answers)
