from rest_framework import serializers

from assignments.models import Assignment, BudgetingTarget, BudgetingTask, OpenTextTask, Section


class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ['id', 'name', 'budget', 'slug', 'status']


class OpenTextTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpenTextTask
        fields = ['question']


class BudgetingTargetSerializer(serializers.ModelSerializer):

    class Meta:
        model = BudgetingTarget
        fields = ['name', 'unit_price', 'reference_amount', 'min_amount', 'max_amount', 'icon']


class BudgetingTaskSerializer(serializers.ModelSerializer):
    targets = BudgetingTargetSerializer(many=True)
    unit = serializers.SerializerMethodField()

    class Meta:
        model = BudgetingTask
        fields = ['name', 'unit', 'targets', 'amount_of_consumption']

    def get_unit(self, obj):
        return obj.get_unit_display()


class SectionSerializer(serializers.ModelSerializer):
    opentexttasks = OpenTextTaskSerializer(many=True)
    budgetingtasks = BudgetingTaskSerializer(many=True)

    class Meta:
        model = Section
        fields = ['id', 'title', 'description', 'video', 'opentexttasks', 'budgetingtasks']
