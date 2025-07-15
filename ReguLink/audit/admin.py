# audit/admin.py
from django.contrib import admin
from .models import AuditLog

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'user', 'action', 'details')
    search_fields = ('user__username', 'action', 'details')
    list_filter = ('action', 'timestamp')
    ordering = ('-timestamp',)