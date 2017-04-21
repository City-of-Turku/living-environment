import pytest
from django.shortcuts import reverse
from rest_framework.test import APIClient

from assignments.models import Assignment, BudgetingTarget, BudgetingTask, OpenTextTask, Section


class TestApi:
    @pytest.mark.django_db
    def test_assignment_endpoint_returns_only_open_assignments(self, create_assignments, assignments_url):
        assert Assignment.objects.count() == 2
        api_client = APIClient()
        response = api_client.get(assignments_url)
        response_data = response.json()
        assert len(response_data) == 1
        assert response_data[0]['status'] == Assignment.STATUS_OPEN

    @pytest.mark.django_db
    def test_all_sections_present_in_open_assignment(self, create_assignments, assignments_url):
        assignment = Assignment.objects.get(status=Assignment.STATUS_OPEN)
        api_client = APIClient()
        response = api_client.get(reverse('assignments:section-list', args=[assignment.slug]))
        response_data = response.json()
        assert len(response_data) == assignment.sections.count()
        for section in response_data:
            assert section['title'] in assignment.sections.values_list('title', flat=True)

    @pytest.mark.django_db
    def test_all_open_text_tasks_present_in_section_for_open_assignment(self, create_assignments, assignments_url):
        assignment = Assignment.objects.get(status=Assignment.STATUS_OPEN)
        api_client = APIClient()
        open_text_tasks = OpenTextTask.objects.filter(section__assignment=assignment)
        for task in open_text_tasks:
            section_url = reverse('assignments:section-detail', args=[assignment.slug, task.section.id])
            response = api_client.get(section_url)
            response_data = response.json()
            found = False
            for data_open_text_task in response_data['opentexttasks']:
                if task.question == data_open_text_task['question']:
                    found = True
                    break
            assert found, 'Cannot find open text task {} in the response'.format(task.question)

    @pytest.mark.django_db
    def test_all_budget_tasks_present_in_section_for_open_assignment(self, create_assignments, assignments_url):
        assignment = Assignment.objects.get(status=Assignment.STATUS_OPEN)
        api_client = APIClient()
        budget_text_tasks = BudgetingTask.objects.filter(section__assignment=assignment)
        for task in budget_text_tasks:
            section_url = reverse('assignments:section-detail', args=[assignment.slug, task.section.id])
            response = api_client.get(section_url)
            response_data = response.json()
            found = False
            for data_budget_text_task in response_data['budgetingtasks']:
                if (
                        task.name == data_budget_text_task['name'] and
                        task.get_unit_display() == data_budget_text_task['unit']
                ):
                    found = True
                    break
            assert found, 'Cannot find budgeting task {} in the response'.format(task.name)

        @pytest.mark.django_db
        def test_all_budget_targets_present_in_budget_tasks_for_open_assignment(self, create_assignments,
                                                                                assignments_url):
            assignment = Assignment.objects.filter(status=Assignment.STATUS_OPEN).first()
            sections = Section.objects.filter(assignment__id=assignment.id)
            for section in sections:
                api_client = APIClient()
                section_url = reverse('assignments:section-detail', args=[assignment.slug, section.id])
                response = api_client.get(section_url)
                response_data = response.json()

                for budget_target in BudgetingTarget.objects.filter(budgeting_tasks__section=section):
                    found_target = False
                    for budget_task in budget_target.budgeting_tasks.all():
                        for data_budget_task in response_data['budgetingtasks']:
                            if budget_task.name == data_budget_task['name']:
                                for data_target in data_budget_task['targets']:
                                    if data_target['name'] == budget_target.name:
                                        found_target = True
                                        break
                            if found_target:
                                break
                        assert found_target, 'Cannot find budgeting target {} in task {}'.format(budget_target.name,
                                                                                                 budget_task.name)
