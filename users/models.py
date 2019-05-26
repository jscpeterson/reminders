from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    def get_email(self, first_name, last_name):
        return '{first}.{last}@da2nd.state.nm.us'.format(first=first_name, last=last_name)

    def get_prosecutor_email(self):
        return self.get_email(self.prosecutor_first_name, self.prosecutor_last_name)

    def get_paralegal_email(self):
        return self.get_email(self.paralegal_first_name, self.paralegal_last_name)

    def get_supervisor_email(self):
        return self.get_email(self.supervisor_first_name, self.supervisor_last_name)


