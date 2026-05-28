"""
Admin configuration for responders
"""
from django.contrib import admin
from .models import Responder, ResponderShift, ResponderAssignment


@admin.register(Responder)
class ResponderAdmin(admin.ModelAdmin):
    list_display = ['name', 'responder_type', 'status', 'available', 'created_at']
    list_filter = ['status', 'responder_type', 'available']
    search_fields = ['name', 'phone', 'email']
    readonly_fields = ['id', 'created_at', 'updated_at', 'last_heartbeat']


@admin.register(ResponderShift)
class ResponderShiftAdmin(admin.ModelAdmin):
    list_display = ['responder', 'shift_start', 'shift_end', 'is_active']
    list_filter = ['is_active', 'shift_start']


@admin.register(ResponderAssignment)
class ResponderAssignmentAdmin(admin.ModelAdmin):
    list_display = ['responder', 'incident', 'assigned_at', 'arrived_at', 'completed_at']
    list_filter = ['assigned_at', 'arrived_at']
