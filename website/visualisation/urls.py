from django.urls import path
from visualisation.views import VisualisationView
app_name = 'visualisation'

urlpatterns = [
    path('render/team/<int:team_id>/',
        VisualisationView.as_view({'get': 'render_team_workout', 'post': 'render_team_workout'}),
        name="render_team_workout"),

]
