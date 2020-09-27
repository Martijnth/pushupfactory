from django.contrib import admin
from workouts.models import Workouts, WorkoutTypes


# Register out own model admin, based on the default UserAdmin
@admin.register(WorkoutTypes)
class WorkoutTypeAdmin(admin.ModelAdmin):
    pass
