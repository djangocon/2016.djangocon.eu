from django.db import models
from django.utils import timezone


class Application(models.Model):
    name = models.CharField(max_length=300)
    email = models.EmailField()
    python_django = models.TextField()
    why = models.TextField()
    financial_assistance = models.TextField()
    location = models.CharField(max_length=150)
    notes = models.TextField(blank=True)

    submitted_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    def as_csv_row(self):
        return (
            self.pk,
            self.name,
            self.email,
            self.python_django,
            self.why,
            self.financial_assistance,
            self.location,
            self.notes,
            self.submitted_on,
        )

    as_csv_row.HEADER = (
        'ID',
        'Name',
        'Email',
        'What do you do with Python/Django',
        'Why do you want to attend',
        'Do you need financial assistance',
        'Location',
        'Notes',
        'Submission date',
    )
