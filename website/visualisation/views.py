from django.db.models import Min
from django.http.response import HttpResponse
from django.utils import timezone
from django.shortcuts import render
from rest_framework import viewsets, authentication, permissions
from rest_framework.response import Response
from workouts.models import Workouts, WorkoutSets, WorkoutTypes
from main.models import Teams, TeamUsers

from datetime import datetime, timedelta

from copy import copy

# Create your views here.
class VisualisationView(viewsets.ViewSet):

    def render_team_workout(self, request, team_id, workout_type_id=None):

        try:
            team = Teams.objects.get(pk=team_id)
        except Teams.DoesNotExist:
            return HttpResponse(status=404)

        start_date = None
        today = timezone.now()
        end_date = timezone.now()

        if start_date is None:
            start_date = Workouts.objects.aggregate(min_date=Min('date'))
            start_date = start_date['min_date']

        if start_date.year < today.year:
            start_date = datetime(today.year, 1, 1, 0, 0, tzinfo=timezone.utc)



        # Get all the workouts for the users in this team
        workout_sets = WorkoutSets.objects.filter(workout__user_id__in=team.users.values('user_id'))

        workout_sets = workout_sets.filter(workout__date__gte=start_date, workout__date__lte=end_date)

        workout_sets = workout_sets.order_by('workout__user_id', 'created_at')

        timestamps = [(start_date + timedelta(days=day_index)).strftime('%Y-%m-%d') for day_index in range((end_date - start_date).days)]

        team_member_result = {team_member[0]: {'name': team_member[1], 'data': [None] * len(timestamps)} for team_member in Workouts.objects.values('user_id').filter(date__gte=start_date, date__lte=end_date).order_by('user_id').distinct().values_list('user_id', 'user__first_name')}

        # result = {(start_date + timedelta(days=day_index)).strftime('%Y-%m-%d'): copy(team_members) for day_index in range((end_date - start_date).days)}
        # print(result)
        # timestamps = []
        # print(result)
        for workout_set in workout_sets:
            set_date = workout_set.workout.date.strftime('%Y-%m-%d')
            day_index = timestamps.index(set_date)
            team_member_result[workout_set.workout.user_id]['data'][day_index] = workout_set.reps if (team_member_result[workout_set.workout.user_id]['data'][day_index] is None or team_member_result[workout_set.workout.user_id]['data'][day_index] < workout_set.reps) and workout_set.reps > 0 else team_member_result[workout_set.workout.user_id]['data'][day_index]
            # print(set_date, workout_set.workout.user_id)
            # result[set_date][workout_set.workout.user_id] = workout_set.reps if result[set_date][workout_set.workout.user_id] is None or result[set_date][workout_set.workout.user_id] < workout_set.reps else result[set_date][workout_set.workout.user_id]
            # user_sets = result['users'].setdefault(workout_set.workout.user_id, {'name': workout_set.workout.user.first_name, 'data': []})
            # user_sets['data'].append(workout_set.reps)

        # result['timestamps'] = sorted(set(timestamps))
        # print(timestamps)
        # print(team_member_result)
        return render(request, 'render_team_workout.html', {'timestamps': timestamps, 'team_members': team_member_result})
