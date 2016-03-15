from django.contrib import admin
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.html import format_html


from .models import Speaker, Talk



def publish(modeladmin, request, queryset):
    """
    Mark the given speakers as published
    """
    updated = queryset.update(published=True)
    messages.success(request, "%s speakers were marked as published" % updated)
    return redirect('admin:speakers_speaker_changelist')

publish.short_description = publish.__doc__


class HasPictureListFilter(admin.SimpleListFilter):
    title = "has picture"
    parameter_name = 'picture'

    def lookups(self, request, model_admin):
        return (
            ('true', 'Yes'),
            ('false', 'No'),
        )

    def queryset(self, request, queryset):
        return {
            'true': queryset.exclude(picture=''),
            'false': queryset.filter(picture=''),
        }.get(self.value())


@admin.register(Speaker)
class SpeakerAdmin(admin.ModelAdmin):
    list_display = ['name', 'talk_title', 'twitter_link', 'github_link', 'published']
    list_filter = ['published', HasPictureListFilter, 'is_keynote', 'mentoring']
    search_fields = ['name', 'talk_title']
    change_list_template = 'smuggler/change_list.html'

    actions = [publish]

    def twitter_link(self, obj):
        if not obj.twitter:
            return None
        return format_html('<a href="{}">@{}</a>', obj.twitter_url, obj.twitter)
    twitter_link.short_description = 'Twitter'
    twitter_link.admin_order_field = 'twitter'

    def github_link(self, obj):
        if not obj.github:
            return None
        return format_html('<a href="{}">{}</a>', obj.github_url, obj.github)
    github_link.short_description = 'Github'
    github_link.admin_order_field = 'github'


@admin.register(Talk)
class TalkAdmin(admin.ModelAdmin):
    list_display = ['weekday', 'time_slot', 'speaker', 'description']
    date_hierarchy = 'day'
    search_fields = ['_description', 'speaker__name', 'speaker__talk_title']
    change_list_template = 'smuggler/change_list.html'

    def weekday(self, obj):
        return obj.weekday
    weekday.short_description = 'Day'
    weekday.admin_order_field = 'day'
