from django.contrib import admin
from django.contrib import messages
from django.shortcuts import redirect

from .models import Speaker



def publish(modeladmin, request, queryset):
    """
    Mark the given speakers as published
    """
    updated = queryset.update(published=True)
    messages.success(request, "%s speakers were marked as published" % updated)
    return redirect('admin:speakers_speaker_changelist')

publish.short_description = publish.__doc__


@admin.register(Speaker)
class SpeakerAdmin(admin.ModelAdmin):
    list_display = ['name', 'talk_title', 'published']
    list_filter = ['published']
    search_fields = ['name', 'talk_title']

    actions = [publish]
