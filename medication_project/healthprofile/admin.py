# admin.py

from django.contrib import admin
from .models import healthProfile, HealthPlan, DailyProgress


@admin.register(healthProfile)
class HealthProfileAdmin(admin.ModelAdmin):
    list_display = ('patient', 'age', 'weight', 'height', 'disease_summary')
    list_filter = ('age', 'disease')
    search_fields = ('patient__name', 'disease', 'addition_info')  # Assuming Patient has a 'name' field
    # readonly_fields = ('patient',)  # Usually, the patient is set once

    def disease_summary(self, obj):
        """Show a truncated version of disease in list view"""
        if obj.disease:
            return (obj.disease[:50] + '...') if len(obj.disease) > 50 else obj.disease
        return '-'
    disease_summary.short_description = 'Disease'


@admin.register(HealthPlan)
class HealthPlanAdmin(admin.ModelAdmin):
    list_display = ('patient', 'generated_at', 'food_chart_preview')
    list_filter = ('generated_at',)
    search_fields = ('patient__name', 'food_chart', 'exercise_plan')
    readonly_fields = ('generated_at',)
    date_hierarchy = 'generated_at'

    def food_chart_preview(self, obj):
        """Short preview of food chart in list view"""
        if obj.food_chart:
            return (obj.food_chart[:60] + '...') if len(obj.food_chart) > 60 else obj.food_chart
        return '-'
    food_chart_preview.short_description = 'Food Chart Preview'


@admin.register(DailyProgress)
class DailyProgressAdmin(admin.ModelAdmin):
    list_display = ('patient', 'date', 'water_intake_liter', 'steps_walked', 'calories_consumed', 'mood')
    list_filter = ('date', 'mood', 'patient')
    search_fields = ('patient__name', 'mood', 'progress_note')
    date_hierarchy = 'date'

    # Optional: Group recent progress by patient using inlines (if you want to see them under HealthProfile)
    # But here it's kept as a separate admin for easy daily tracking