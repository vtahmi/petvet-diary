from django.contrib import admin
from .models import Pet, Vaccination, HealthCondition


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ['name', 'species', 'owner', 'date_of_birth', 'age']
    list_filter = ['species', 'created_at']
    search_fields = ['name', 'owner__username']

    readonly_fields = ['age', 'created_at']


@admin.register(Vaccination)
class VaccinationAdmin(admin.ModelAdmin):
    list_display = ['vaccine_name', 'pet', 'date_given', 'next_due_date']
    list_filter = ['date_given']
    search_fields = ['vaccine_name', 'pet__name']


@admin.register(HealthCondition)
class HealthConditionAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    filter_horizontal = ['pets']
