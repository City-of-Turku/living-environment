import pytest
from django.shortcuts import reverse

from assignments.models import Assignment, Section
from assignments.tests.factories import (
    AssignmentFactory, BudgetingTargetAnswerFactory, BudgetingTargetFactory, BudgetingTaskFactory,
    OpenTextAnswerFactory, OpenTextTaskFactory, SchoolClassFactory, SchoolFactory, SectionFactory, SubmissionFactory,
    VoluntaryTaskFactory
)


@pytest.fixture
def create_assignments():
    assignment_1 = AssignmentFactory()
    assignment_2 = AssignmentFactory(status=Assignment.STATUS_CLOSED)
    section_1 = SectionFactory(assignment=assignment_1)
    section_2 = SectionFactory(assignment=assignment_1)
    section_3 = SectionFactory(assignment=assignment_1)
    SectionFactory(assignment=assignment_2)
    OpenTextTaskFactory(section=section_1)
    OpenTextTaskFactory(section=section_1)
    first_target = BudgetingTargetFactory()
    sec_target = BudgetingTargetFactory()
    BudgetingTaskFactory(section=section_2, targets=(first_target, sec_target))
    BudgetingTaskFactory(section=section_1, targets=(first_target, sec_target))
    VoluntaryTaskFactory(section=section_3)


@pytest.fixture
def assignments_url():
    return reverse('assignment-list')


@pytest.fixture
def answers_submit_data():
    class_1 = SchoolClassFactory()
    class_2 = SchoolClassFactory()
    school = SchoolFactory(classes=(class_1, class_2))
    assignment = AssignmentFactory(schools=(school,))
    section = SectionFactory(assignment=assignment)
    open_text_task_1 = OpenTextTaskFactory(section=section)
    open_text_task_2 = OpenTextTaskFactory(section=section)
    first_target = BudgetingTargetFactory()
    sec_target = BudgetingTargetFactory()
    budgeting_task = BudgetingTaskFactory(section=section, targets=(first_target, sec_target))

    return {
        "school": school.id,
        "school_class": class_1.id,
        "open_text_tasks": [
            {
                "task": open_text_task_1.id,
                "answer": "First answer"
            },
            {
                "task": open_text_task_2.id,
                "answer": "Second answer"
            }
        ],
        "budgeting_targets": [
            {
                "task": budgeting_task.id,
                "target": first_target.id,
                "amount": 200,
                "point": [123.343, 444.1232]
            }
        ]
    }


@pytest.fixture
def answers_submit_with_voluntary_data(answers_submit_data):
    section = Section.objects.first()
    voluntary_signup_task = VoluntaryTaskFactory(section=section)
    answers_submit_data['voluntary_tasks'] = [
        {
            "task": voluntary_signup_task.id,
            "first_name": "first",
            "last_name": "last",
            "email": "test@test.com",
            "phone": "43423",
            "description": "school/class",
            "lat": 60.192059,
            "long": 24.945831
        },
        {
            "task": voluntary_signup_task.id,
            "first_name": "first",
            "last_name": "last",
            "email": "test@test.com",
            "phone": "43423",
            "description": "school/class",
            "lat": 60.192059,
            "long": 24.945831
        }
    ]
    return answers_submit_data


@pytest.fixture
def answers():
    class_1 = SchoolClassFactory()
    class_2 = SchoolClassFactory()
    school = SchoolFactory(classes=(class_1, class_2))
    assignment = AssignmentFactory(schools=(school,))
    section = SectionFactory(assignment=assignment)
    section_2 = SectionFactory(assignment=assignment)
    submission = SubmissionFactory(school=school)
    open_text_task = OpenTextTaskFactory(section=section)
    OpenTextAnswerFactory(submission=submission, task=open_text_task)
    budgeting_target_1 = BudgetingTargetFactory()
    budgeting_target_2 = BudgetingTargetFactory()
    budgeting_task = BudgetingTaskFactory(section=section_2, targets=(budgeting_target_1, budgeting_target_2))
    BudgetingTargetAnswerFactory(task=budgeting_task, target=budgeting_target_1, submission=submission)
    BudgetingTargetAnswerFactory(task=budgeting_task, target=budgeting_target_2, submission=submission)
