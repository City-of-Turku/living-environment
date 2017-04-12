from django.db import models
from django.utils.translation import ugettext as _
from ckeditor_uploader.fields import RichTextUploadingField
from djgeojson.fields import GeometryField


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
    slug = models.SlugField(max_length=80, unique=True)

    class Meta:
        verbose_name = _('assignment')
        verbose_name_plural = _('assignments')

    def __str__(self):
        return self.name


class Section(models.Model):
    """
    Section is a part of assignment with tasks related to it.
    """
    title = models.CharField(_('title'), max_length=256)
    description = RichTextUploadingField(_('description'), blank=True)
    assignment = models.ForeignKey(Assignment, related_name='sections')
    video = models.URLField(null=True, blank=True)

    class Meta:
        verbose_name = _('section')
        verbose_name_plural = _('sections')

    def __str__(self):
        return 'Section: {}'.format(self.title)


class OpenTextTask(models.Model):
    """
    Simple question task where the answer is placed in text area
    """
    section = models.ForeignKey(Section, related_name='open_text_tasks')
    question = models.TextField()

    class Meta:
        verbose_name = _('open text task')
        verbose_name_plural = _('open text tasks')

    def __str__(self):
        return 'Question: {}'.format(self.question)

