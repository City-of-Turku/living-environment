import factory
import factory.fuzzy
import random

from django.contrib.auth.models import User
from django.utils.text import slugify
from assignments import models

class FuzzyArea(factory.fuzzy.BaseFuzzyAttribute):
    def __init__(self, min, max, **defaults):
        super(FuzzyArea, self).__init__(**defaults)
        self.min = min
        self.max = max

    def fuzz(self):
        return {
            'x': random.randint(self.min, self.max),
            'y': random.randint(self.min, self.max)
        }

class AssignmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Assignment
        skip_postgeneration_save = True

    name = factory.Sequence(lambda n: 'assignment_%s' % n)
    status = models.Assignment.STATUS_OPEN
    budget = factory.fuzzy.FuzzyDecimal(10000, 30000, precision=2)
    slug = factory.LazyAttribute(lambda n: slugify(n.name))
    area = FuzzyArea(-100, 100)

    @factory.post_generation
    def schools(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for school in extracted:
                self.schools.add(school)


class SectionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Section

    title = factory.Sequence(lambda n: 'section_%s' % n)
    description = factory.fuzzy.FuzzyText(length=50)
    assignment = factory.SubFactory(AssignmentFactory)
    video = 'http://testvideo.com'
    order_number = factory.fuzzy.FuzzyInteger(0, 100)


class OpenTextTaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.OpenTextTask

    question = factory.fuzzy.FuzzyText()
    section = factory.SubFactory(SectionFactory)
    order_number = factory.fuzzy.FuzzyInteger(0, 100)


class BudgetingTargetFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.BudgetingTarget

    name = factory.Sequence(lambda n: 'target_%s' % n)
    unit_price = factory.fuzzy.FuzzyDecimal(2, 15, precision=2)
    max_amount = factory.fuzzy.FuzzyDecimal(0, 10, precision=2)


class BudgetingTaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.BudgetingTask
        skip_postgeneration_save = True

    section = factory.SubFactory(SectionFactory)
    name = factory.Sequence(lambda n: 'budgetingtask_%s' % n)
    amount_of_consumption = factory.fuzzy.FuzzyDecimal(2, 100, precision=2)
    unit = factory.Iterator([models.BudgetingTask.UNIT_HA, models.BudgetingTask.UNIT_PCS])
    order_number = factory.fuzzy.FuzzyInteger(0, 100)

    @factory.post_generation
    def targets(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for target in extracted:
                self.targets.add(target)


class VoluntaryTaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.VoluntarySignupTask

    name = factory.fuzzy.FuzzyText()
    section = factory.SubFactory(SectionFactory)
    order_number = factory.fuzzy.FuzzyInteger(0, 100)


class SchoolFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.School
        skip_postgeneration_save = True

    name = factory.Sequence(lambda n: 'school_%s' % n)

    @factory.post_generation
    def classes(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for school_class in extracted:
                self.classes.add(school_class)


class SchoolClassFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.SchoolClass

    name = factory.Sequence(lambda n: 'class_%s' % n)


class SubmissionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Submission

    school = factory.SubFactory(SchoolFactory)
    school_class = factory.SubFactory(SchoolClassFactory)


class OpenTextAnswerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.OpenTextAnswer

    submission = factory.SubFactory(SubmissionFactory)
    task = factory.SubFactory(OpenTextTaskFactory)
    answer = factory.fuzzy.FuzzyText()


class BudgetingTargetAnswerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.BudgetingTargetAnswer

    submission = factory.SubFactory(SubmissionFactory)
    task = factory.SubFactory(BudgetingTaskFactory)
    target = factory.SubFactory(BudgetingTargetFactory)
    amount = factory.fuzzy.FuzzyDecimal(2, 20, precision=2)
    point = '{"type": "Point", "coordinates": [100, 200]}'


class AdminFactory(factory.Factory):
    class Meta:
        model = User

    first_name = 'Admin'
    last_name = 'User'
    is_staff = True
