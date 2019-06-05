from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    SUPERVISOR = 1
    PROSECUTOR = 2
    PARALEGAL = 3
    POSITION_CHOICES = (
        (SUPERVISOR, 'Supervisor'),
        (PROSECUTOR, 'Prosecutor'),
        (PARALEGAL, 'Paralegal')
    )
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    position = models.IntegerField(choices=POSITION_CHOICES, null=True)

    def __str__(self):
        display_name = self.first_name + " " + self.last_name
        return display_name
