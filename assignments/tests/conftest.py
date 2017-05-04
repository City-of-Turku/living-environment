import pytest
from django.shortcuts import reverse

from assignments.models import Assignment
from assignments.tests.factories import (
    AssignmentFactory, BudgetingTargetAnswerFactory, BudgetingTargetFactory, BudgetingTaskFactory,
    OpenTextAnswerFactory, OpenTextTaskFactory, SchoolClassFactory, SchoolFactory, SectionFactory, SubmissionFactory
)


@pytest.fixture
def create_assignments():
    assignment_1 = AssignmentFactory()
    assignment_2 = AssignmentFactory(status=Assignment.STATUS_CLOSED)
    section_1 = SectionFactory(assignment=assignment_1)
    section_2 = SectionFactory(assignment=assignment_1)
    SectionFactory(assignment=assignment_2)
    OpenTextTaskFactory(section=section_1)
    first_target = BudgetingTargetFactory()
    sec_target = BudgetingTargetFactory()
    BudgetingTaskFactory(section=section_2, targets=(first_target, sec_target))


@pytest.fixture
def assignments_url():
    return reverse('assignments:assignment-list')


@pytest.fixture
def answers_submit_data():
    assignment = AssignmentFactory()
    class_1 = SchoolClassFactory()
    class_2 = SchoolClassFactory()
    school = SchoolFactory(assignment=assignment, classes=(class_1, class_2))
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
def answers():
    assignment = AssignmentFactory()
    section = SectionFactory(assignment=assignment)
    section_2 = SectionFactory(assignment=assignment)
    class_1 = SchoolClassFactory()
    class_2 = SchoolClassFactory()
    school = SchoolFactory(assignment=assignment, classes=(class_1, class_2))
    submission = SubmissionFactory(school=school)
    open_text_task = OpenTextTaskFactory(section=section)
    OpenTextAnswerFactory(submission=submission, task=open_text_task)
    budgeting_target_1 = BudgetingTargetFactory()
    budgeting_target_2 = BudgetingTargetFactory()
    budgeting_task = BudgetingTaskFactory(section=section_2, targets=(budgeting_target_1, budgeting_target_2))
    BudgetingTargetAnswerFactory(task=budgeting_task, target=budgeting_target_1, submission=submission)
    BudgetingTargetAnswerFactory(task=budgeting_task, target=budgeting_target_2, submission=submission)


@pytest.fixture
def voluntary_signup_data():
    return {
        "first_name": "first",
        "last_name": "sec",
        "email": "s@fdasd.com",
        "phone": "43423",
        "description": "school/class",
        "lat": 60.192059,
        "long": 24.945831
    }
