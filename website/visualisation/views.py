from django.http.response import HttpResponse
from django.utils import timezone
from django.shortcuts import render
from rest_framework import viewsets, authentication, permissions
from rest_framework.response import Response
from workouts.models import Workouts, WorkoutSets, WorkoutTypes
from main.models import Teams, TeamUsers

from datetime import datetime


# Create your views here.
class VisualisationView(viewsets.ViewSet):

    def render_team_workout(self, request, team_id, workout_type_id):

        try:
            team = Teams.objects.get(pk=team_id)
        except Teams.DoesNotExist:
            return HttpResponse(status=404)

        start_date = None
        end_date = timezone.now()

        # Get all the workouts for the users in this team
        workout_sets = WorkoutSets.objects.filter(workout__user_id__in=team.users.values('user_id'))

        if start_date is not None:
            workout_sets = workout_sets.filter(workout__date__gte=start_date)

        if end_date is not None:
            workout_sets = workout_sets.filter(workout__date__lte=end_date)

        workout_sets = workout_sets.order_by('workout__user_id', 'created_at')

        result = {
            'timestamps': [],
            'users': {},
        }
        timestamps = []
        for workout_set in workout_sets:
            timestamps.append(workout_set.workout.date.strftime('%Y-%m-%d'))
            user_sets = result['users'].setdefault(workout_set.workout.user_id, {'name': workout_set.workout.user.first_name, 'data': []})
            user_sets['data'].append(workout_set.reps)

        result['timestamps'] = sorted(set(timestamps))
        # print(result)
        # workouts.delete()
        # print(workout_sets)
        # workout = request.data.get('workout', None)
        # if workout is None:
        #     return Response({'message':' You need to specify a workout in the post request'}, status=500)

        # for workout_type_id, sets in workout.items():
        #     workout = Workouts.objects.create(user=request.user, workout_type_id=workout_type_id)
        #     for reps in sets:
        #         WorkoutSets.objects.create(workout=workout, reps=reps)

        # print(request.user, request.data)
        return render(request, 'render_team_workout.html', {'graph_data': result})
