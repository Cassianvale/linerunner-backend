from django.contrib import admin
from .models import Bugtracker


@admin.register(Bugtracker)
class BugtrackerAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'attachment', 'type', 'severity', 'module', 'handler', 'state']
