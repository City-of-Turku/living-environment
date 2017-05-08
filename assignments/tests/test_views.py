import json
from collections import defaultdict
from unittest.mock import patch

import pytest
from django.shortcuts import reverse
from django.test import override_settings
from rest_framework import status
from rest_framework.test import APIClient

from assignments.models import (
    Assignment, BudgetingTarget, BudgetingTargetAnswer, BudgetingTask, OpenTextAnswer, OpenTextTask, Submission, Task,
    VoluntarySignupTask
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
    def test_all_tasks_present_in_section_for_open_assignment(self, create_assignments):
        assignment = Assignment.objects.get(status=Assignment.STATUS_OPEN)
        api_client = APIClient()
        sections = assignment.sections.all()
        ids_per_section_db = []
        for section in sections:
            tasks_ids = Task.objects.filter(section=section).values_list('id', flat=True)
            ids_per_section_db.append((section.id, list(tasks_ids)))
        response = api_client.get(reverse('assignments:assignment-detail', args=[assignment.slug]))
        response_data = response.json()
        ids_per_section_response = []
        for section in response_data['sections']:
            tasks_response_ids = []
            for task in section['tasks']:
                tasks_response_ids.append(task['id'])
            ids_per_section_response.append((section['id'], tasks_response_ids))
        assert ids_per_section_db == ids_per_section_response

    @pytest.mark.django_db
    def test_all_sections_sorted_by_order_number(self, create_assignments):
        assignment = Assignment.objects.get(status=Assignment.STATUS_OPEN)
        sections_order_no = assignment.sections.values_list('order_number', flat=True)
        assert sorted(list(sections_order_no)) == list(sections_order_no)

    @pytest.mark.django_db
    def test_all_tasks_sorted_by_order_number_in_sections(self, create_assignments):
        assignment = Assignment.objects.get(status=Assignment.STATUS_OPEN)
        sections = assignment.sections.all()
        for section in sections:
            tasks_order_no = Task.objects.filter(section=section).values_list('order_number', flat=True)
            assert sorted(list(tasks_order_no)) == list(tasks_order_no)

    @pytest.mark.django_db
    def test_all_open_text_tasks_present_in_section_for_open_assignment(self, create_assignments):
        assignment = Assignment.objects.get(status=Assignment.STATUS_OPEN)
        api_client = APIClient()
        open_text_tasks_ids = OpenTextTask.objects.filter(section__assignment=assignment).values_list('id', flat=True)
        response = api_client.get(reverse('assignments:assignment-detail', args=[assignment.slug]))
        response_data = response.json()
        open_text_tasks_response_ids = []
        for section in response_data['sections']:
            for task in section['tasks']:
                if task['task_type'] == 'open_text_task':
                    open_text_tasks_response_ids.append(task['id'])
        assert sorted(list(open_text_tasks_ids)) == sorted(open_text_tasks_response_ids)

    @pytest.mark.django_db
    def test_all_budget_tasks_present_in_section_for_open_assignment(self, create_assignments):
        assignment = Assignment.objects.get(status=Assignment.STATUS_OPEN)
        api_client = APIClient()
        budget_tasks_ids = BudgetingTask.objects.filter(section__assignment=assignment).values_list('id', flat=True)
        response = api_client.get(reverse('assignments:assignment-detail', args=[assignment.slug]))
        response_data = response.json()
        budgeting_tasks_response_ids = []
        for section in response_data['sections']:
            for task in section['tasks']:
                if task['task_type'] == 'budgeting_task':
                    budgeting_tasks_response_ids.append(task['id'])
        assert sorted(list(budget_tasks_ids)) == sorted(budgeting_tasks_response_ids)

    @pytest.mark.django_db
    def test_all_voluntary_tasks_present_in_section_for_open_assignment(self, create_assignments):
        assignment = Assignment.objects.get(status=Assignment.STATUS_OPEN)
        api_client = APIClient()
        voluntary_tasks_ids = VoluntarySignupTask.objects.filter(section__assignment=assignment).values_list('id',
                                                                                                             flat=True)
        response = api_client.get(reverse('assignments:assignment-detail', args=[assignment.slug]))
        response_data = response.json()
        voluntary_tasks_response_ids = []
        for section in response_data['sections']:
            for task in section['tasks']:
                if task['task_type'] == 'voluntary_signup_task':
                    voluntary_tasks_response_ids.append(task['id'])
        assert sorted(list(voluntary_tasks_ids)) == sorted(voluntary_tasks_response_ids)

    @pytest.mark.django_db
    def test_all_budget_targets_present_in_budget_tasks_for_open_assignment(self, create_assignments,
                                                                            assignments_url):
        assignment = Assignment.objects.get(status=Assignment.STATUS_OPEN)
        api_client = APIClient()
        budgeting_targets_ids = BudgetingTarget.objects.filter(
            budgeting_tasks__section__assignment=assignment).values_list('id', flat=True)
        response = api_client.get(reverse('assignments:assignment-detail', args=[assignment.slug]))
        response_data = response.json()
        budgeting_targets_response_ids = []
        for section in response_data['sections']:
            for task in section['tasks']:
                if task['task_type'] == 'budgeting_task':
                    budgeting_targets_response_ids.extend([target['id'] for target in task['data']['targets']])
        assert sorted(list(budgeting_targets_ids)) == sorted(budgeting_targets_response_ids)

    @pytest.mark.django_db
    def test_open_text_answers_school_data_saved_successfully(self, answers_submit_data):
        api_client = APIClient()
        assignment = Assignment.objects.get()
        answers_url = reverse('assignments:answers', args=[assignment.slug])
        api_client.post(answers_url, json.dumps(answers_submit_data), content_type='application/json')
        open_text_answers = OpenTextAnswer.objects.all()
        open_text_school_no = open_text_answers.filter(
            submission__school=answers_submit_data['school'],
            submission__school_class=answers_submit_data['school_class']).count()
        assert len(open_text_answers) == open_text_school_no

    @pytest.mark.django_db
    def test_budgeting_answers_school_data_saved_successfully(self, answers_submit_data):
        api_client = APIClient()
        assignment = Assignment.objects.get()
        answers_url = reverse('assignments:answers', args=[assignment.slug])
        api_client.post(answers_url, json.dumps(answers_submit_data), content_type='application/json')
        budgeting_answers = BudgetingTargetAnswer.objects.all()
        budgeting_answers_school_no = budgeting_answers.filter(
            submission__school=answers_submit_data['school'],
            submission__school_class=answers_submit_data['school_class']).count()
        assert len(budgeting_answers) == budgeting_answers_school_no

    @pytest.mark.django_db
    def test_answers_data_open_text_submitted_successfully(self, answers_submit_data):
        api_client = APIClient()
        assignment = Assignment.objects.get()
        answers_url = reverse('assignments:answers', args=[assignment.slug])
        api_client.post(answers_url, json.dumps(answers_submit_data), content_type='application/json')
        for open_text_answer in answers_submit_data['open_text_tasks']:
            task = OpenTextTask.objects.filter(id=open_text_answer['task']).first()
            assert task is not None
            assert task.open_text_answers.filter(answer=open_text_answer['answer']).exists()

    @pytest.mark.django_db
    def test_answers_data_budgeting_targets_submitted_successfully(self, answers_submit_data):
        api_client = APIClient()
        assignment = Assignment.objects.get()
        answers_url = reverse('assignments:answers', args=[assignment.slug])
        api_client.post(answers_url, json.dumps(answers_submit_data), content_type='application/json')
        for budgeting_target in answers_submit_data['budgeting_targets']:
            task = BudgetingTask.objects.filter(id=budgeting_target['task']).first()
            target = BudgetingTarget.objects.filter(id=budgeting_target['target']).first()
            assert task is not None
            assert target is not None
            assert task.budgeting_answers.filter(task=task, target=target, amount=budgeting_target['amount'],
                                                 point={'type': 'Point',
                                                        'coordinates': budgeting_target['point']}).exists()

    @pytest.mark.django_db
    @override_settings(FEEDBACK_SYSTEM_URL='http://test-feedback/')
    def test_answers_data_voluntary_signup_submitted_successfully(self, answers_submit_with_voluntary_data):
        api_client = APIClient()
        assignment = Assignment.objects.get()
        answers_url = reverse('assignments:answers', args=[assignment.slug])
        with patch('assignments.helper.urllib.request.urlopen') as urlopen_mock:
            api_client.post(answers_url, json.dumps(answers_submit_with_voluntary_data),
                            content_type='application/json')
        assert urlopen_mock.called

    @pytest.mark.django_db
    @override_settings(FEEDBACK_SYSTEM_URL='http://test-feedback/')
    def test_validation_failed_with_incorrect_voluntary_signup_post_data(self, answers_submit_with_voluntary_data):
        voluntary_signup_data = answers_submit_with_voluntary_data['voluntary_tasks']
        voluntary_signup_data[0].pop('lat')
        api_client = APIClient()
        assignment = Assignment.objects.get()
        answers_url = reverse('assignments:answers', args=[assignment.slug])
        with patch('assignments.helper.urllib.request.urlopen'):
            response = api_client.post(answers_url, json.dumps(answers_submit_with_voluntary_data),
                                       content_type='application/json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.django_db
    def test_bad_missing_submission_data_failed_to_save(self, answers_submit_data):
        api_client = APIClient()
        assignment = Assignment.objects.get()
        answers_url = reverse('assignments:answers', args=[assignment.slug])
        answers_submit_data.pop('school')
        response = api_client.post(answers_url, json.dumps(answers_submit_data), content_type='application/json')
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
        answers_url = reverse('assignments:answers', args=[assignment.slug])
        response = api_client.post(answers_url, json.dumps(answers_submit_data), content_type='application/json')
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
        answers_url = reverse('assignments:answers', args=[assignment.slug])
        response = api_client.post(answers_url, json.dumps(answers_submit_data), content_type='application/json')
        assert response.status_code == status.HTTP_201_CREATED

    @pytest.mark.django_db
    def test_report_with_wrong_assignment_slug_not_found(self, answers):
        api_client = APIClient()
        answers_url = reverse('assignments:answers', args=['fake_assignment'])
        response = api_client.get(answers_url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.django_db
    def test_report_submissions_count_correct(self, answers):
        api_client = APIClient()
        assignment = Assignment.objects.get()
        answers_url = reverse('assignments:answers', args=[assignment.slug])
        response = api_client.get(answers_url)
        response_data = response.json()
        submissions = {
            'schools': defaultdict(int),
            'classes': defaultdict(int)
        }
        for submission in Submission.objects.all():
            submissions['schools'][submission.school.name] += 1
            submissions['classes'][submission.school_class.name] += 1
        for submission_response in response_data['submissions']['per_school']:
            assert submissions['schools'][submission_response['school__name']] == submission_response['count']
        for submission_response in response_data['submissions']['per_class']:
            assert submissions['classes'][submission_response['school_class__name']] == submission_response['count']
        assert len(submissions['schools']) == len(response_data['submissions']['per_school'])
        assert len(submissions['classes']) == len(response_data['submissions']['per_class'])

    @pytest.mark.django_db
    def test_report_contains_all_open_text_answers(self, answers):
        api_client = APIClient()
        assignment = Assignment.objects.get()
        answers_url = reverse('assignments:answers', args=[assignment.slug])
        response = api_client.get(answers_url)
        response_data = response.json()
        open_text_answers_ids = OpenTextAnswer.objects.filter(
            task__section__assignment=assignment).values_list('id', flat=True)

        report_answers_ids = []
        for section_data in response_data['sections']:
            for open_text_task_data in section_data['open_text_tasks']:
                for answer_data in open_text_task_data['answers']:
                    report_answers_ids.append(answer_data['id'])
        assert sorted(list(open_text_answers_ids)) == sorted(report_answers_ids)

    @pytest.mark.django_db
    def test_report_contains_all_budgeting_answers(self, answers):
        api_client = APIClient()
        assignment = Assignment.objects.get()
        answers_url = reverse('assignments:answers', args=[assignment.slug])
        response = api_client.get(answers_url)
        response_data = response.json()
        budgeting_answers_ids = BudgetingTargetAnswer.objects.filter(
            task__section__assignment=assignment).values_list('id', flat=True)

        report_answers_ids = []
        for section_data in response_data['sections']:
            for budgeting_task in section_data['budgeting_tasks']:
                for answer_data in budgeting_task['answers']:
                    report_answers_ids.append(answer_data['id'])
        assert sorted(list(budgeting_answers_ids)) == sorted(report_answers_ids)
