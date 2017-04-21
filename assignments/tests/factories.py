import factory
import factory.fuzzy
from django.utils.text import slugify
from psycopg2.extras import NumericRange

from assignments import models


class AssignmentFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Assignment

    name = factory.Sequence(lambda n: 'assignment_%s' % n)
    status = models.Assignment.STATUS_OPEN
    budget = factory.fuzzy.FuzzyDecimal(10000, 30000, precision=2)
    slug = factory.LazyAttribute(lambda n: slugify(n.name))


class SectionFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Section

    title = factory.Sequence(lambda n: 'section_%s' % n)
    description = factory.fuzzy.FuzzyText(length=50)
    assignment = factory.SubFactory(AssignmentFactory)
    video = 'http://testvideo.com'


class OpenTextTaskFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.OpenTextTask

    question = factory.fuzzy.FuzzyText()
    section = factory.SubFactory(SectionFactory)


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

    @factory.post_generation
    def targets(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for target in extracted:
                self.targets.add(target)
