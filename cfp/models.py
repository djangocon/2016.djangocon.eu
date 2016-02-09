from django.db import models
from django.utils import timezone


class BaseProposal(models.Model):
    class SKILL_LEVEL:
        EVERYONE = 1
        NOVICE = 2
        INTERMEDIATE = 3
        ADVANCED = 4

        choices = [
            (EVERYONE, 'everyone'),
            (NOVICE, 'novice'),
            (INTERMEDIATE, 'intermediate'),
            (ADVANCED, 'advanced'),
        ]

    name = models.CharField(max_length=200)
    email = models.EmailField()
    speaker_information = models.TextField(blank=True)
    title = models.TextField()
    description = models.TextField()
    audience = models.TextField()
    props = models.TextField(blank=True)
    skill_level = models.PositiveIntegerField(choices=SKILL_LEVEL.choices, default=SKILL_LEVEL.EVERYONE)
    notes = models.TextField(blank=True)
    mentoring = models.BooleanField(default=False)

    selected = models.BooleanField(default=False)

    submitted_on = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

    def as_csv_row(self, anonymized=False):
        return (
            self.pk,
            'proposal %s' % self.pk if anonymized else self.name,
            'proposal%s@proposals.djangocon.eu' % self.pk if anonymized else self.email,
            self.title,
            self.description,
            self.audience,
            self.get_skill_level_display(),
            self.notes,
        )

    as_csv_row.HEADER = (
        'ID',
        'Name',
        'Email',
        'Title',
        'Description',
        'Audience',
        'Skill level',
        'Notes',
    )


class Proposal(BaseProposal):
    pass


class WorkshopProposal(BaseProposal):
    class Meta:
        verbose_name = 'workshop proposal'
        verbose_name_plural = 'workshop proposals'
