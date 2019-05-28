from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    POSITION_CHOICES = (
        (1, 'Supervisor'),
        (2, 'Prosecutor'),
        (3, 'Paralegal')
    )

    def get_email_format(self, first_name, last_name):
        return '{first}.{last}@da2nd.state.nm.us'.format(first=first_name.lower(), last=last_name.lower())

    def get_email(self):
        return self.get_email_format((self._first_name.lower()), self._last_name.lower())

    first_name = models.CharField(max_length=60, null=True, blank=True)
    last_name = models.CharField(max_length=60, null=True, blank=True)

    position = models.IntegerField(choices=POSITION_CHOICES, null=True, blank=True)
