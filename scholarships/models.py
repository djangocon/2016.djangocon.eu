from django.db import models
from django.utils import timezone


class Application(models.Model):
    name = models.CharField(max_length=300)
    email = models.EmailField()
    python_django = models.TextField()
    why = models.TextField()
    financial_assistance = models.CharField(max_length=150, blank=True)
    location = models.CharField(max_length=150)
    notes = models.TextField(blank=True)

    submitted_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
