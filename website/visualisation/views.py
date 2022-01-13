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
        start_date = request.data.get('start_date', request.session.get('start_date', None))
        end_date = request.data.get('end_date', request.session.get('end_date', None))
        show_daily_totals = request.data.get('show_daily_totals', request.session.get('show_daily_totals', False))
        workout_type_id = int(request.data.get('workout_type_id', request.session.get('workout_type_id', 1)))

        if len(request.data) > 0:
            if start_date == '':
                start_date = None
                request.session['start_date'] = None
            else:
                request.session['start_date'] = start_date

            if end_date == '':
                end_date = None
                request.session['end_date'] = None
            else:
                request.session['end_date'] = end_date

            if show_daily_totals == 'on':
                show_daily_totals = True
                request.session['show_daily_totals'] = True
            else:
                show_daily_totals = False
                request.session['show_daily_totals'] = False

            request.session['workout_type_id'] = workout_type_id
            request.session.MODIFIED = True

        try:
            team = Teams.objects.get(pk=team_id)
        except Teams.DoesNotExist:
            return HttpResponse(status=404)

        # Convert from string...lazy..
        if start_date is not None:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').replace(tzinfo=timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
        if end_date is not None:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').replace(tzinfo=timezone.utc).replace(hour=23, minute=59, second=0, microsecond=0)

        if end_date is None:
            end_date = timezone.now().replace(hour=23, minute=59, second=0, microsecond=0)

        if start_date is None:
            start_date = Workouts.objects.aggregate(min_date=Min('date'))
            start_date = start_date['min_date']

        # Get all the workouts for the users in this team
        workout_sets = WorkoutSets.objects.filter(workout__workout_type_id=workout_type_id, workout__user_id__in=team.users.values('user_id'))

        workout_sets = workout_sets.filter(workout__date__gte=start_date, workout__date__lte=end_date)

        workout_sets = workout_sets.order_by('workout__user_id', 'created_at')

        timestamps = [(start_date + timedelta(days=day_index)).strftime('%Y-%m-%d') for day_index in range((end_date - start_date).days + 1)]

        team_member_result = {
            team_member[0]: {
                'name': team_member[1],
                'data': [None] * len(timestamps)
            } for team_member in Workouts.objects.values('user_id').filter(date__gte=start_date, date__lte=end_date).order_by('user_id').distinct().values_list('user_id', 'user__first_name')
        }

        for workout_set in workout_sets:
            set_date = workout_set.workout.date.strftime('%Y-%m-%d')
            day_index = timestamps.index(set_date)
            if show_daily_totals is False:
                if (team_member_result[workout_set.workout.user_id]['data'][day_index] is None or team_member_result[workout_set.workout.user_id]['data'][day_index] < workout_set.reps) and workout_set.reps > 0:
                    team_member_result[workout_set.workout.user_id]['data'][day_index] = workout_set.reps

            # Aggregate them (maybe we can do this in the SQL)
            else:
                if team_member_result[workout_set.workout.user_id]['data'][day_index] is None:
                    team_member_result[workout_set.workout.user_id]['data'][day_index] = workout_set.reps
                else:
                    team_member_result[workout_set.workout.user_id]['data'][day_index] += workout_set.reps

        return render(request, 'render_team_workout.html', {
            'timestamps': timestamps,
            'team_members': team_member_result,
            'team_id': team_id,
            'start_date': request.session.get('start_date', None),
            'end_date': request.session.get('end_date', None),
            'show_daily_totals': show_daily_totals,
            'workout_type_id': workout_type_id,
            'workout_types': WorkoutTypes.objects.all(),
        })


