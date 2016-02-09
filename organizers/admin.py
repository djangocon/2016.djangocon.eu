from django.contrib import admin

from .models import Organizer


@admin.register(Organizer)
class OrganizerAdmin(admin.ModelAdmin):
    list_display = ['name', 'title', 'emoji', 'published']
    list_filter = ['published']
    search_fields = ['name', 'title', 'description']
