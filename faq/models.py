from django.db import models
from django.utils.html import format_html


class QuestionCategory(models.Model):
    name = models.CharField(max_length=50)
    emoji_alt = models.CharField(max_length=5, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    @property
    def data_emoji_alt(self):
        if not self.emoji_alt:
            return ''
        return format_html('data-emoji-alt="{}"', self.emoji_alt)


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
