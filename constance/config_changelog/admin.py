from django.contrib import admin

from constance.config_changelog.models import ConfigLogEntry


class ConfigLogEntryAdmin(admin.ModelAdmin):
    list_display = ('key', 'old_value', 'new_value', 'changed_at')


admin.site.register(ConfigLogEntry, ConfigLogEntryAdmin)