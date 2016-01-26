from django.db import models


class QuestionCategory(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Question(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField(blank=True)
    category = models.ForeignKey(QuestionCategory, blank=True, null=True)
    published = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question

    def has_answer(self):
        return bool(self.answer)