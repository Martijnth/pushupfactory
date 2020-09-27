from django.db import models
from main.models import Users, Teams


class WorkoutTypes(models.Model):
    """
        Pushups for example is a workout type
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    name = models.CharField(max_length=100, blank=False, null=False)


class Workouts(models.Model):
    """
        Base workout model. A workout should always have SETS connected.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    deleted = models.BooleanField(default=False)

    user = models.ForeignKey(Users, blank=False, null=False, on_delete=models.CASCADE)
    workout_type = models.ForeignKey(WorkoutTypes, blank=False, null=False, on_delete=models.CASCADE)

class WorkoutSets(models.Model):
    """
        The workout sets keep track of the reps made in this set.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    workout = models.ForeignKey(Workouts, blank=False, null=False, on_delete=models.CASCADE)

    reps = models.IntegerField(default=0)

