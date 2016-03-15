from django.contrib import admin

from .models import Workshop


@admin.register(Workshop)
class WorkshopAdmin(admin.ModelAdmin):
    list_display = ['weekday', 'time_slot', 'author', 'title_html']
    date_hierarchy = 'day'
    search_fields = ['_description', '_author', '_title']
    change_list_template = 'smuggler/change_list.html'

    def weekday(self, obj):
        return obj.weekday
    weekday.short_description = 'Day'
    weekday.admin_order_field = 'day'
