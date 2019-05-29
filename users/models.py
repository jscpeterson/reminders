from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    POSITION_CHOICES = (
        (1, 'Supervisor'),
        (2, 'Prosecutor'),
        (3, 'Paralegal')
    )
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    position = models.IntegerField(null=True)

    def __str__(self):
        display_name = self.first_name + " " + self.last_name
        return display_name
