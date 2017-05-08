import factory
import factory.fuzzy
from django.utils.text import slugify

from assignments import models


class AssignmentFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Assignment

    name = factory.Sequence(lambda n: 'assignment_%s' % n)
    status = models.Assignment.STATUS_OPEN
    budget = factory.fuzzy.FuzzyDecimal(10000, 30000, precision=2)
    slug = factory.LazyAttribute(lambda n: slugify(n.name))

    @factory.post_generation
    def schools(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for school in extracted:
                self.schools.add(school)


class SectionFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Section

    title = factory.Sequence(lambda n: 'section_%s' % n)
    description = factory.fuzzy.FuzzyText(length=50)
    assignment = factory.SubFactory(AssignmentFactory)
    video = 'http://testvideo.com'
    order_number = factory.fuzzy.FuzzyInteger(0, 100)


class OpenTextTaskFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.OpenTextTask

    question = factory.fuzzy.FuzzyText()
    section = factory.SubFactory(SectionFactory)
    order_number = factory.fuzzy.FuzzyInteger(0, 100)


class BudgetingTargetFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.BudgetingTarget

    name = factory.Sequence(lambda n: 'target_%s' % n)
    unit_price = factory.fuzzy.FuzzyDecimal(2, 15, precision=2)
    max_amount = factory.fuzzy.FuzzyDecimal(0, 10, precision=2)


class BudgetingTaskFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.BudgetingTask

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


class SchoolFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.School

    name = factory.Sequence(lambda n: 'school_%s' % n)

    @factory.post_generation
    def classes(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for school_class in extracted:
                self.classes.add(school_class)


class SchoolClassFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.SchoolClass

    name = factory.Sequence(lambda n: 'class_%s' % n)


class SubmissionFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Submission

    school = factory.SubFactory(SchoolFactory)
    school_class = factory.SubFactory(SchoolClassFactory)


class OpenTextAnswerFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.OpenTextAnswer

    submission = factory.SubFactory(SubmissionFactory)
    task = factory.SubFactory(OpenTextTaskFactory)
    answer = factory.fuzzy.FuzzyText()


class BudgetingTargetAnswerFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.BudgetingTargetAnswer

    submission = factory.SubFactory(SubmissionFactory)
    task = factory.SubFactory(BudgetingTaskFactory)
    target = factory.SubFactory(BudgetingTargetFactory)
    amount = factory.fuzzy.FuzzyDecimal(2, 20, precision=2)
    point = '{"type": "Point", "coordinates": [100, 200]}'
