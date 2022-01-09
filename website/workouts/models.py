from django.db import models
from main.models import Users


class WorkoutTypesManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by('name')


class WorkoutTypes(models.Model):
    """
        Pushups for example is a workout type
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    name = models.CharField(max_length=100, blank=False, null=False)

    objects = WorkoutTypesManager()

    def __str__(self):
        return f'<WorkoutType: {self.name}>'


class Workouts(models.Model):
    """
        Base workout model. A workout should always have SETS connected.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    date = models.DateTimeField(blank=False, null=False)

    deleted = models.BooleanField(default=False)

    user = models.ForeignKey(Users, blank=False, null=False, on_delete=models.CASCADE)
    workout_type = models.ForeignKey(WorkoutTypes, blank=False, null=False, on_delete=models.CASCADE)


class WorkoutSetsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().\
            select_related('workout').\
            select_related('workout__workout_type').\
            select_related('workout__user')


class WorkoutSets(models.Model):
    """
        The workout sets keep track of the reps made in this set.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    workout = models.ForeignKey(Workouts, blank=False, null=False, on_delete=models.CASCADE)

    reps = models.IntegerField(default=0)

    objects = WorkoutSetsManager()

    def __str__(self):
        return '{} did {} reps of the type `{}`'.format(self.workout.user.first_name, self.reps, self.workout.workout_type.name)
