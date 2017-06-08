from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from djgeojson.fields import GeometryField, PointField
from polymorphic.models import PolymorphicModel

from assignments.fields import SortedAsSelectedManyToManyField


class Assignment(models.Model):
    """
    Assignment is a top level concept of the application.
    Every assignment consists of several sections.
    It is uniquely identified by name
    """
    STATUS_OPEN = 0
    STATUS_CLOSED = 1
    STATUS_CHOICES = (
        (STATUS_OPEN, _('Open')),
        (STATUS_CLOSED, _('Closed'))
    )

    name = models.CharField(_('name'), max_length=128, unique=True)
    header = models.CharField(_('header'), max_length=255, null=True)
    description = RichTextUploadingField(_('description'), blank=True)
    image = models.ImageField(_('image'), upload_to='assignment/image/',
                              blank=True, null=True)
    area = GeometryField(_('area'))
    status = models.IntegerField(_('status'), choices=STATUS_CHOICES, default=STATUS_OPEN)
    budget = models.DecimalField(_('budget'), max_digits=10, decimal_places=2, default=0)
    schools = models.ManyToManyField('School', related_name='assignments', verbose_name=_('schools'))
    slug = models.SlugField(max_length=80, unique=True)

    class Meta:
        verbose_name = _('Assignment')
        verbose_name_plural = _('Assignments')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return '{}/{}/'.format(settings.FRONTEND_APP_URL, self.slug)

    def get_submissions(self, school=None, school_class=None):
        """
        Get all submissions related to the assignment filtered by school or school_class if given.
        """
        submissions = Submission.objects.all()
        if school:
            submissions = submissions.filter(school=school)
        if school_class:
            submissions = submissions.filter(school_class=school_class)
        return submissions


class Section(models.Model):
    """
    Section is a part of assignment with tasks related to it.
    """
    title = models.CharField(_('title'), max_length=255)
    description = RichTextUploadingField(_('description'), blank=True)
    assignment = models.ForeignKey(Assignment, related_name='sections', verbose_name=_('Assignment'))
    video = models.URLField(null=True, blank=True)
    order_number = models.IntegerField(_('order number'), default=0,
                                       help_text=_('Order in which sections are shown'))

    class Meta:
        verbose_name = _('Section')
        verbose_name_plural = _('Sections')
        ordering = ['order_number', 'title']

    def __str__(self):
        return self.title


class Task(PolymorphicModel):
    """
    Parent model for all task types.
    """
    section = models.ForeignKey(Section, related_name='tasks', on_delete=models.CASCADE)
    order_number = models.IntegerField(_('order number'), default=0, help_text=_('Order in which tasks are shown'))

    class Meta:
        ordering = ['order_number']
        # Fix delete.
        # Workaround for https://github.com/django-polymorphic/django-polymorphic/issues/229#issuecomment-246613138
        base_manager_name = 'base_objects'

    @property
    def task_type(self):
        return 'basic_task'


class OpenTextTask(Task):
    """
    Simple question task where the answer is placed in text area
    """
    question = models.TextField(_('question'))

    class Meta:
        verbose_name = _('open text task')
        verbose_name_plural = _('open text tasks')

    def get_answers(self, school=None, school_class=None):
        """
        Get open text answers filtered by school and class
        """
        answers = self.open_text_answers.all()
        if school:
            answers = answers.filter(submission__school=school)
        if school_class:
            answers = answers.filter(submission__school_class=school_class)
        return answers

    @property
    def task_type(self):
        return 'open_text_task'

    def __str__(self):
        return self.question[:80]


class BudgetingTarget(models.Model):
    """
    Budget task targets. Not all the fields have to be defined here. Reference amount refers to official amount spent
    on this target. Min and max amount should be defined for targets with value in a certain range.
    """

    name = models.CharField(_('name'), max_length=255)
    unit_price = models.DecimalField(_('price'), max_digits=10, decimal_places=2, default=0)
    reference_amount = models.DecimalField(_('reference amount'), max_digits=10, decimal_places=2, default=0)
    min_amount = models.DecimalField(_('min amount'), max_digits=10, decimal_places=2, default=0)
    max_amount = models.DecimalField(_('max amount'), max_digits=10, decimal_places=2, null=True, blank=True)
    icon = models.FileField(_('icon'), upload_to='target/icons/', blank=True, null=True)

    class Meta:
        verbose_name = _('budget target')
        verbose_name_plural = _('budget targets')

    def __str__(self):
        return self.name


class BudgetingTask(Task):
    """
    Budget tasks are related to section and consists of one or more Budgeting targets
    """
    UNIT_HA = 0
    UNIT_PCS = 1
    UNIT_CHOICES = (
        (UNIT_HA, _('ha')),
        (UNIT_PCS, _('pcs'))
    )
    TEXT_TYPE = 0
    MAP_TYPE = 1
    TYPE_CHOICES = (
        (TEXT_TYPE, _('text')),
        (MAP_TYPE, _('map'))
    )

    name = models.CharField(_('name'), max_length=255)
    unit = models.IntegerField(_('unit'), choices=UNIT_CHOICES, default=UNIT_HA)
    amount_of_consumption = models.DecimalField(_('amount of consumption'), max_digits=10, decimal_places=2,
                                                help_text=_('Number of units required to be spent on the task'),
                                                default=0)
    targets = SortedAsSelectedManyToManyField(BudgetingTarget, related_name='budgeting_tasks',
                                              verbose_name=_('budget targets'))
    budgeting_type = models.IntegerField(_('type'), choices=TYPE_CHOICES, default=TEXT_TYPE)

    class Meta:
        verbose_name = _('budgeting task')
        verbose_name_plural = _('budgeting tasks')

    def get_answers(self, school=None, school_class=None):
        """
        Get budgeting task answers filtered by school and class
        """
        answers = self.budgeting_answers.all()
        if school:
            answers = answers.filter(submission__school=school)
        if school_class:
            answers = answers.filter(submission__school_class=school_class)
        return answers

    @property
    def task_type(self):
        return 'budgeting_task'

    def __str__(self):
        return self.name


class SchoolClass(models.Model):
    name = models.CharField(_('name'), max_length=255)

    class Meta:
        verbose_name = _('class')
        verbose_name_plural = _('classes')

    def __str__(self):
        return self.name


class School(models.Model):
    name = models.CharField(_('name'), max_length=255)
    classes = models.ManyToManyField(SchoolClass, related_name='schools', verbose_name=_('classes'))

    class Meta:
        verbose_name = _('school')
        verbose_name_plural = _('schools')

    def __str__(self):
        return self.name


class Submission(models.Model):
    school = models.ForeignKey(School, related_name='%(class)ss')
    school_class = models.ForeignKey(SchoolClass, related_name='%(class)ss')


class OpenTextAnswer(models.Model):
    """
    Answer on OpenTextTask
    """

    submission = models.ForeignKey(Submission, related_name='open_text_answers')
    task = models.ForeignKey(OpenTextTask, related_name='open_text_answers')
    answer = models.TextField()


class BudgetingTargetAnswer(models.Model):
    """
    Answer on BudgetingTarget. We set references to both task and target, in order to
    uniquely connect budgeting answer with related task
    """

    submission = models.ForeignKey(Submission, related_name='budgeting_answers')
    task = models.ForeignKey(BudgetingTask, related_name='budgeting_answers')
    target = models.ForeignKey(BudgetingTarget, related_name='budgeting_answers')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    point = PointField(null=True, blank=True)


class VoluntarySignupTask(Task):
    """
    Task defines voluntary actions participant can submit to.
    """
    name = models.CharField(_('name'), max_length=255)

    class Meta:
        verbose_name = _('voluntary signup task')
        verbose_name_plural = _('voluntary signup tasks')

    @property
    def task_type(self):
        return 'voluntary_signup_task'

    def __str__(self):
        return self.name
