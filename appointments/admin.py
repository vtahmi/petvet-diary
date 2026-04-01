from django.contrib import admin
from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['pet', 'owner', 'veterinarian', 'appointment_date', 'status']
    list_filter = ['status', 'appointment_date']
    search_fields = ['pet__name', 'owner__username', 'reason']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Appointment Details', {
            'fields': ('pet', 'owner', 'veterinarian', 'appointment_date', 'reason')
        }),
        ('Status & Notes', {
            'fields': ('status', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )