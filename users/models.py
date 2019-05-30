from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    SUP = 'Supervisor'
    PRO = 'Prosecutor'
    PAR = 'Paralegal'
    POSITION_CHOICES = (
        (SUP, 'Supervisor'),
        (PRO, 'Prosecutor'),
        (PAR, 'Paralegal')
    )
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    position = models.CharField(choices=POSITION_CHOICES, max_length=3)

    def __str__(self):
        display_name = self.first_name + " " + self.last_name
        return display_name
