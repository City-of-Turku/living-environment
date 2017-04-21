import pytest
from django.shortcuts import reverse

from assignments.models import Assignment
from assignments.tests.factories import (
    AssignmentFactory, BudgetingTargetFactory, BudgetingTaskFactory, OpenTextTaskFactory, SectionFactory
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
