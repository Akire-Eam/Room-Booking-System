from django.contrib import admin

from .models import *


class ActivityLogAdmin(admin.ModelAdmin):
    # Fields that should be read-only in the admin interface
    readonly_fields = ('action', 'log', 'timestamp')
    list_display = ('id', 'action', 'log', 'timestamp')
    list_display_links = ('id', 'action', 'log', 'timestamp')

    # Override the get_readonly_fields method to make all fields read-only
    def get_readonly_fields(self, request, obj=None):
        return self.readonly_fields


# Register your models here.
admin.site.register(ActivityLog, ActivityLogAdmin)
