from django.contrib import admin

from .models import Application

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'financial_assistance', 'location', 'submitted_on')
    list_per_page = 200

# Register your models here.
