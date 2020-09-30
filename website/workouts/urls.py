from django.urls import path
from workouts.views import WorkoutsAPI, quick_import
app_name = 'workouts'

urlpatterns = [
    path('api/v1/workout/add/',
        WorkoutsAPI.as_view({'post': 'add_workout'}),
        name="admin_api_workout"),

    path('quick_import/',
        quick_import,
        name="admin_api_workout"),

]
