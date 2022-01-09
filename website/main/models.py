from django.db import models

from django.contrib.auth.models import AbstractUser


class Users(AbstractUser):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    deleted = models.BooleanField(default=False)


class Teams(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100, blank=False, null=False)
    deleted = models.BooleanField(default=False)

    @property
    def users(self):
        return TeamUsers.objects.filter(team=self)


class TeamUsers(models.Model):

    PERMISSION_TYPE_MEMBER = 0
    PERMISSION_TYPE_VP = 1
    PERMISSION_TYPE_OWNER = 2

    PERMISSION_TYPE_CHOICES = (
        (PERMISSION_TYPE_MEMBER, 'Member'),
        (PERMISSION_TYPE_VP, 'Vice President'),
        (PERMISSION_TYPE_MEMBER, 'Owner'),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(Users, blank=False, null=False, on_delete=models.CASCADE)
    team = models.ForeignKey(Teams, blank=False, null=False, on_delete=models.CASCADE)

    permission_type = models.IntegerField(choices=PERMISSION_TYPE_CHOICES, blank=False, default=PERMISSION_TYPE_MEMBER)
