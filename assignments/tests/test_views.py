import json

import pytest
from django.shortcuts import reverse
from rest_framework import status
from rest_framework.test import APIClient

from assignments.models import (
    Assignment, BudgetingTarget, BudgetingTargetAnswer, BudgetingTask, OpenTextAnswer, OpenTextTask
)


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
    def test_all_sections_present_in_open_assignment(self, create_assignments):
        assignment = Assignment.objects.get(status=Assignment.STATUS_OPEN)
        api_client = APIClient()
        section_ids = assignment.sections.values_list('id', flat=True)
        response = api_client.get(reverse('assignments:assignment-detail', args=[assignment.slug]))
        response_data = response.json()
        sections_response_ids = []
        for section in response_data['sections']:
            sections_response_ids.append(section['id'])
        assert list(section_ids).sort() == sections_response_ids.sort()

    @pytest.mark.django_db
    def test_all_open_text_tasks_present_in_section_for_open_assignment(self, create_assignments):
        assignment = Assignment.objects.get(status=Assignment.STATUS_OPEN)
        api_client = APIClient()
        open_text_tasks_ids = OpenTextTask.objects.filter(section__assignment=assignment).values_list('id', flat=True)
        response = api_client.get(reverse('assignments:assignment-detail', args=[assignment.slug]))
        response_data = response.json()
        open_text_tasks_response_ids = []
        for section in response_data['sections']:
            for open_text_task in section['open_text_tasks']:
                open_text_tasks_response_ids.append(open_text_task['id'])
        assert list(open_text_tasks_ids).sort() == open_text_tasks_response_ids.sort()

    @pytest.mark.django_db
    def test_all_budget_tasks_present_in_section_for_open_assignment(self, create_assignments):
        assignment = Assignment.objects.get(status=Assignment.STATUS_OPEN)
        api_client = APIClient()
        budget_tasks_ids = BudgetingTask.objects.filter(section__assignment=assignment).values_list('id', flat=True)
        response = api_client.get(reverse('assignments:assignment-detail', args=[assignment.slug]))
        response_data = response.json()
        budgeting_tasks_response_ids = []
        for section in response_data['sections']:
            for budgeting_text_task in section['budgeting_tasks']:
                budgeting_tasks_response_ids.append(budgeting_text_task['id'])
        assert list(budget_tasks_ids).sort() == budgeting_tasks_response_ids.sort()

    @pytest.mark.django_db
    def test_all_budget_targets_present_in_budget_tasks_for_open_assignment(self, create_assignments,
                                                                            assignments_url):
        assignment = Assignment.objects.get(status=Assignment.STATUS_OPEN)
        api_client = APIClient()
        budgeting_targets_ids = BudgetingTarget.objects.filter(budgeting_tasks__section__assignment=assignment
                                                           ).values_list('id', flat=True)
        response = api_client.get(reverse('assignments:assignment-detail', args=[assignment.slug]))
        response_data = response.json()
        budgeting_targets_response_ids = []
        for section in response_data['sections']:
            for budgeting_task in section['budgeting_tasks']:
                budgeting_targets_response_ids.append([target['id'] for target in budgeting_task['targets']])
        assert list(budgeting_targets_ids).sort() == budgeting_targets_response_ids.sort()

    @pytest.mark.django_db
    def test_open_text_answers_school_data_saved_successfully(self, answers_submit_data):
        api_client = APIClient()
        assignment = Assignment.objects.get()
        section_url = reverse('assignments:answers', args=[assignment.slug])
        response = api_client.post(section_url, json.dumps(answers_submit_data), content_type='application/json')
        open_text_answers = OpenTextAnswer.objects.all()
        open_text_school_no = open_text_answers.filter(student__school=answers_submit_data['school'],
                                                       student__school_class=answers_submit_data['school_class']).count()
        assert len(open_text_answers) == open_text_school_no

    @pytest.mark.django_db
    def test_budgeting_answers_school_data_saved_successfully(self, answers_submit_data):
        api_client = APIClient()
        assignment = Assignment.objects.get()
        section_url = reverse('assignments:answers', args=[assignment.slug])
        response = api_client.post(section_url, json.dumps(answers_submit_data), content_type='application/json')
        budgeting_answers = BudgetingTargetAnswer.objects.all()
        budgeting_answers_school_no = budgeting_answers.filter(student__school=answers_submit_data['school'],
                                                       student__school_class=answers_submit_data['school_class']).count()
        assert len(budgeting_answers) == budgeting_answers_school_no

    @pytest.mark.django_db
    def test_answers_data_open_text_submitted_successfully(self, answers_submit_data):
        api_client = APIClient()
        assignment = Assignment.objects.get()
        section_url = reverse('assignments:answers', args=[assignment.slug])
        response = api_client.post(section_url, json.dumps(answers_submit_data), content_type='application/json')
        for open_text_answer in answers_submit_data['open_text_tasks']:
            task = OpenTextTask.objects.filter(id=open_text_answer['task']).first()
            assert task is not None
            assert task.open_text_answers.filter(answer=open_text_answer['answer']).exists()

    @pytest.mark.django_db
    def test_answers_data_bugdeting_targets_submitted_successfully(self, answers_submit_data):
        api_client = APIClient()
        assignment = Assignment.objects.get()
        section_url = reverse('assignments:answers', args=[assignment.slug])
        response = api_client.post(section_url, json.dumps(answers_submit_data), content_type='application/json')
        for budgeting_target in answers_submit_data['budgeting_targets']:
            task = BudgetingTask.objects.filter(id=budgeting_target['task']).first()
            target = BudgetingTarget.objects.filter(id=budgeting_target['target']).first()
            assert task is not None
            assert target is not None
            assert task.budgeting_answers.filter(task=task, target=target, amount=budgeting_target['amount'],
                                                 point={'type': 'Point',
                                                        'coordinates': budgeting_target['point']}).exists()

    @pytest.mark.django_db
    def test_bad_missing_student_data_failed_to_save(self, answers_submit_data):
        api_client = APIClient()
        assignment = Assignment.objects.get()
        section_url = reverse('assignments:answers', args=[assignment.slug])
        answers_submit_data.pop('school')
        response = api_client.post(section_url, json.dumps(answers_submit_data), content_type='application/json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert OpenTextAnswer.objects.count() == 0
        assert BudgetingTargetAnswer.objects.count() == 0

    @pytest.mark.django_db
    def test_bad_structured_answers_failed_to_save(self, answers_submit_data):
        answers_submit_data['open_text_tasks'].append({
            'badstructured': 'fake task',
            'answer': 'No answer'
        })
        api_client = APIClient()
        assignment = Assignment.objects.get()
        section_url = reverse('assignments:answers', args=[assignment.slug])
        response = api_client.post(section_url, json.dumps(answers_submit_data), content_type='application/json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert BudgetingTargetAnswer.objects.count() == 0
        assert OpenTextAnswer.objects.count() == 0

    @pytest.mark.django_db
    def test_answer_data_with_missing_target_point_saved(self, answers_submit_data):
        targets = answers_submit_data['budgeting_targets']
        changed_target = targets[0]
        changed_target.pop('point')
        changed_targets = [changed_target] + targets[1:]
        answers_submit_data['budgeting_targets'] = changed_targets
        api_client = APIClient()
        assignment = Assignment.objects.get()
        section_url = reverse('assignments:answers', args=[assignment.slug])
        response = api_client.post(section_url, json.dumps(answers_submit_data), content_type='application/json')
        assert response.status_code == status.HTTP_201_CREATED
