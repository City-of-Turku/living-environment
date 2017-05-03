from django.db import models
from django.shortcuts import reverse
from django.utils.translation import ugettext_lazy as _

from ckeditor_uploader.fields import RichTextUploadingField
from djgeojson.fields import GeometryField, PointField


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
    area = GeometryField(_('area'))
    status = models.IntegerField(_('status'), choices=STATUS_CHOICES, default=STATUS_OPEN)
    budget = models.DecimalField(_('budget'), max_digits=10, decimal_places=2, default=0)
    slug = models.SlugField(max_length=80, unique=True,
                            help_text=_('The user-friendly URL identifier ex. www.example.com/runosmaen-koulu'))

    class Meta:
        verbose_name = _('Assignment')
        verbose_name_plural = _('Assignments')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('assignments:assignment-detail', args=[self.slug])

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
    title = models.CharField(_('title'), max_length=256)
    description = RichTextUploadingField(_('description'), blank=True)
    assignment = models.ForeignKey(Assignment, related_name='sections', verbose_name=_('Assignment'))
    video = models.URLField(null=True, blank=True)

    class Meta:
        verbose_name = _('Section')
        verbose_name_plural = _('Sections')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('assignments:section-detail', args=[self.assignment.slug, self.pk])


class BaseTask(models.Model):
    """
    Abstract model for all tasks.
    """
    section = models.ForeignKey(Section, related_name='%(class)ss')

    class Meta:
        abstract = True


class OpenTextTask(BaseTask):
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
            answers = answers.filter(submission__school__name=school)
        if school_class:
            answers = answers.filter(submission__school_class__name=school_class)
        return answers


class BudgetingTarget(models.Model):
    """
    Budget task targets. Not all the fields have to be defined here. Reference amount refers to official amount spent
    on this target. Min and max amount should be defined for targets with value in a certain range.
    """

    name = models.CharField(_('name'), max_length=256)
    unit_price = models.DecimalField(_('price'), max_digits=10, decimal_places=2, default=0)
    reference_amount = models.DecimalField(_('reference amount'), max_digits=10, decimal_places=2, default=0)
    min_amount = models.DecimalField(_('min amount'), max_digits=10, decimal_places=2, default=0)
    max_amount = models.DecimalField(_('max amount'), max_digits=10, decimal_places=2, null=True, blank=True)
    icon = models.FileField(_('icon'), upload_to='target/icons/', blank=True, default='target/icons/default.png')

    class Meta:
        verbose_name = _('budget target')
        verbose_name_plural = _('budget targets')

    def __str__(self):
        return self.name


class BudgetingTask(BaseTask):
    """
    Budget tasks are related to section and consists of one or more Budgeting targets
    """
    UNIT_HA = 0
    UNIT_PCS = 1
    UNIT_CHOICES = (
        (UNIT_HA, _('ha')),
        (UNIT_PCS, _('pcs'))
    )

    name = models.CharField(_('name'), max_length=256)
    unit = models.IntegerField(_('unit'), choices=UNIT_CHOICES, default=UNIT_HA)
    amount_of_consumption = models.DecimalField(_('amount of consumption'), max_digits=10, decimal_places=2,
                                                help_text=_('Number of units required to be spent on the task'),
                                                default=0)
    targets = models.ManyToManyField(BudgetingTarget, related_name='budgeting_tasks', verbose_name=_('budget targets'))

    class Meta:
        verbose_name = _('budgeting task')
        verbose_name_plural = _('budgeting tasks')

    def __str__(self):
        return self.name

    def get_answers(self, school=None, school_class=None):
        """
        Get budgeting task answers filtered by school and class
        """
        answers = self.budgeting_answers.all()
        if school:
            answers = answers.filter(submission__school__name=school)
        if school_class:
            answers = answers.filter(submission__school_class__name=school_class)
        return answers


class SchoolClass(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = _('class')
        verbose_name_plural = _('classes')

    def __str__(self):
        return self.name


class School(models.Model):
    name = models.CharField(max_length=255)
    assignment = models.ForeignKey(Assignment, related_name='schools')
    classes = models.ManyToManyField(SchoolClass, related_name='schools')

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
