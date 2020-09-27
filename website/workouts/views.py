from django.shortcuts import render
from rest_framework import viewsets, authentication, permissions
from rest_framework.response import Response
from workouts.models import Workouts, WorkoutSets

# Create your views here.
class WorkoutsAPI(viewsets.ViewSet):

    authentication_classes = [authentication.TokenAuthentication]
    def add_workout(self, request):
        if request.user.is_anonymous:
            return Response(status=404)

        workout = request.data.get('workout', None)
        if workout is None:
            return Response({'message':' You need to specify a workout in the post request'}, status=500)

        for workout_type_id, sets in workout.items():
            workout = Workouts.objects.create(user=request.user, workout_type_id=workout_type_id)
            for reps in sets:
                WorkoutSets.objects.create(workout=workout, reps=reps)

        print(request.user, request.data)
        return Response()
