from django.urls import path
from workouts.views import WorkoutsAPI, WorkoutsView
app_name = 'workouts'

urlpatterns = [
    path('api/v1/workout/add/',
        WorkoutsAPI.as_view({'post': 'add_workout'}),
        name="admin_api_workout"),

    path('workouts/', WorkoutsView.as_view({'get': 'render_workouts', 'post': 'save_workouts'}), name='workouts'),
    # path('workouts/', WorkoutsView.as_view({}), name='save_workouts'),-
]
