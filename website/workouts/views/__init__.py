from django.shortcuts import render

from rest_framework import viewsets, authentication
from rest_framework.response import Response
from workouts.models import Workouts, WorkoutSets, WorkoutTypes

from datetime import datetime, timedelta
import json


# Create your views here.
class WorkoutsAPI(viewsets.ViewSet):

    authentication_classes = [authentication.TokenAuthentication]

    def add_workout(self, request):
        if request.user.is_anonymous:
            return Response(status=404)

        workout = request.data.get('workout', None)
        if workout is None:
            return Response({'message': 'You need to specify a `workout` in the post request'}, status=500)

        if type(workout) is str:
            workout = json.loads(workout)

        date_time = request.data.get('date', None)
        if date_time is None or len(date_time) != 16:
            return Response({'message': 'You need to specify a correct `datetime` in the post request: yyyy-mm-dd hh:mm'}, status=500)
        try:
            date, time = date_time.split(' ')
            date = datetime(*(int(date_item) for date_item in date.split('-')), *(int(time_item) for time_item in time.split(':')))
        except Exception as error:
            return Response({'message': 'Invalid date: {}'.format(error)}, status=500)

        try:
            for workout_type_id, sets in workout.items():
                workout = Workouts.objects.create(user=request.user, workout_type_id=workout_type_id, date=date)
                for reps in sets:
                    WorkoutSets.objects.create(workout=workout, reps=reps)
        except Exception as error:
            return Response({'message': 'Error: {}'.format(error)}, status=500)

        return Response()

class WorkoutsView(viewsets.ViewSet):

    def render_workouts(self, request):
        most_used_workout_types = WorkoutTypes.objects.filter(pk__in=Workouts.objects.filter(user=request.user).values('workout_type_id').distinct())
        other_workout_types = WorkoutTypes.objects.exclude(pk__in=most_used_workout_types)
        return render(request, 'workouts/index.html', {'most_used_workout_types': most_used_workout_types, 'other_workout_types': other_workout_types})

    def save_workouts(self, request):
        workout_type_id = request.data.get('workout_type_id', None)
        amount = request.data.get('amount', None)
        if workout_type_id is not None and amount is not None:
            try:
                current_workout = Workouts.objects.get(user=request.user, workout_type_id=workout_type_id, date__gte=datetime.now() - timedelta(minutes=30))
            except Workouts.DoesNotExist:
                current_workout = Workouts.objects.create(user=request.user, workout_type_id=workout_type_id, date=datetime.now())

            WorkoutSets.objects.create(workout=current_workout, reps=amount)
            print(request.data)
        return self.render_workouts(request)
