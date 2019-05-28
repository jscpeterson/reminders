from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):

    prosecutor_name = models.CharField(max_length=60, null=True, blank=True)
    paralegal_name = models.CharField(max_length=60, null=True, blank=True)
    supervisor_name = models.CharField(max_length=60, null=True, blank=True)
    email = models.EmailField(max_length=254)




