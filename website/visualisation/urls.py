from django.urls import path
from visualisation.views import VisualisationView
app_name = 'visualisation'

urlpatterns = [
    path('render/teams/<int:team_id>/<int:workout_type_id>/',
        VisualisationView.as_view({'get': 'render_team_workout'}),
        name="render_team_workout"),

]
