from django.http.response import HttpResponse
from django.utils.timezone import timezone
from django.shortcuts import render
from rest_framework import viewsets, authentication, permissions
from rest_framework.response import Response
from workouts.models import Workouts, WorkoutSets

from datetime import datetime


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

def quick_import(request):
    # Workouts.objects.all().delete()
    return HttpResponse(status=404)
    labels = ['2020-05-13', '2020-05-14', '2020-05-15', '2020-05-18', '2020-05-19', '2020-05-20', '2020-05-21', '2020-05-22', '2020-05-25', '2020-05-26', '2020-05-27', '2020-05-28', '2020-05-29', '2020-06-01', '2020-06-02', '2020-06-03', '2020-06-04', '2020-06-05', '2020-06-08', '2020-06-09', '2020-06-10', '2020-06-11', '2020-06-12', '2020-06-15', '2020-06-16', '2020-06-17', '2020-06-18', '2020-06-19', '2020-06-22', '2020-06-23', '2020-06-24', '2020-06-25', '2020-06-26', '2020-06-29', '2020-06-30', '2020-07-01', '2020-07-02', '2020-07-03', '2020-07-06', '2020-07-07', '2020-07-08', '2020-07-09', '2020-07-10', '2020-07-13', '2020-07-14', '2020-07-15', '2020-07-16', '2020-07-17', '2020-07-20', '2020-07-21', '2020-07-22', '2020-07-23', '2020-07-24', '2020-07-27', '2020-07-28', '2020-07-29', '2020-07-30', '2020-07-31', '2020-08-03', '2020-08-04', '2020-08-05', '2020-08-06', '2020-08-07', '2020-08-10', '2020-08-11', '2020-08-12', '2020-08-13', '2020-08-14', '2020-08-17', '2020-08-18', '2020-08-19', '2020-08-20', '2020-08-21', '2020-08-24', '2020-08-25', '2020-08-26', '2020-08-27', '2020-08-28', '2020-08-31', '2020-09-01', '2020-09-02', '2020-09-03', '2020-09-04', '2020-09-07', '2020-09-08', '2020-09-09', '2020-09-10', '2020-09-11', '2020-09-14', '2020-09-15', '2020-09-16', '2020-09-17', '2020-09-18', '2020-09-21', '2020-09-22', '2020-09-23', '2020-09-24', '2020-09-25', '2020-09-28', '2020-09-29', ]
    values = {
        4: [25, 27, 27, 17, 27, 27, 26, 28, 27, 28, 27, 29, 30, 35, 29, 29, 31, 30, 25, 30, 30, 29, 28, 27, 30, 29, 28, 28, 31, 29, 27, 31, 27, 30, 28, 29, 30, 30, 30, 29, 30, 30, 31, 30, 30, 31, 33, 32, 29, 29, 29, 30, 31, 33, 30, 27, 27, 28, 35, 35, 37, 39, 36, 38, 35, 25, 25, 33, 33, 34, 29, 29, 37, 29, 27, 30, 29, 30, 28, 28, 25, 30, 31, 29, 30, 29, 28, 27, 33, 31, 34, 31, 35, 34, 27, 33,  33, 35, 34, 34, ],
        2: [24, 26, 20, 21, 22, 21, 25, 27, 20, 14, 23, 21, 20, 25, 26, 25, 24, 21, 26, 28, 20, 22, 25, 27, 30,  8,  2, 31, 24, 25, 20, 25, 27, 21, 20, 20, 25, 28, 25, 24, 24, 0, 22, 30, 25, 0, 26, 26, 22, 24, 25, 22, 25, 25, 28, 30, 30, 31, 26, 28, 30, 32, 28, 28, 29, 28, 27, 30, 31, 26, 23, 27, 20, 22, 0, 25,  28, 0, 20, 23, 27, 26, 30, 0, 0, 32, 19, 26, 0, 30, 31, 23, 23, 10, 31, 0, 0, 31, 26, 25,],
        3: [23, 22, 24, 21, 22, 24, 25, 24, 24, 22, 24, 27, 25, 0, 22, 24, 25, 0, 20, 24, 24, 26, 27, 27, 30, 25, 28, 29, 27, 26, 27, 24, 30, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 21, 25, 0, 26, 25, 26, 25, 0, 24, 27, 0, 26, 0, 0, 0, 25, 25, 24, 22, 0, 0, 0, 25, 25, 27, 25, 24, 0, 0, 0, 27, 0, 24, 0, 26, 24, 0, 26, 24, 26, 0, 0, 26, 21, 24, 26, 26, 27, 0, 25, 24, 23, 24, 0, 24, 25, 24, ],
        1: [42, 45, 47, 50, 51, 52, 53, 53, 42, 53, 54, 55, 47, 50, 55, 27, 57, 57, 60, 60, 61, 62, 55, 27, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 44, 45, 46, 47, 48, 50, 51, 52, 7, 8, 5, 9, 10, 5, 6, 11, 10, 12, 10, 12, 13, 14, 15, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 7, 5, 10, 10, 0, 2, 0, 0, 50, 0, 0, 35, 45, 40,  30, 0, 33, 0, 35, 40, 45, 0, 0, 0, 51, 67, 70, 0 ],
    }

    for index, date in enumerate(labels):
        created_at = datetime(*[int(date_item) for date_item in date.split('-')], 12, tzinfo=timezone.utc)
        for user_id, reps in values.items():
            workout = Workouts.objects.create(date=created_at, user_id=user_id, workout_type_id=1)

            workout_set = WorkoutSets.objects.create(created_at=created_at, updated_at=created_at, workout=workout, reps=reps[index])

        # print(index, date)

    return HttpResponse()