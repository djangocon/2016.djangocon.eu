from django.contrib import admin
from django.contrib import messages
from django.shortcuts import redirect

from .models import Question, QuestionCategory

def publish(modeladmin, request, queryset):
    """
    Mark the given question as published
    """
    updated = queryset.update(published=True)
    messages.success(request, "%s questions were marked as published" % updated)
    return redirect('admin:faq_question_changelist')

publish.short_description = publish.__doc__


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question', 'created', 'has_answer', 'published']
    actions = [publish]

    def has_answer(self, obj):
        return obj.has_answer()
    has_answer.boolean = True
    has_answer.admin_order_field = 'has_answer'


@admin.register(QuestionCategory)
class QuestionCategoryAdmin(admin.ModelAdmin):
    pass
