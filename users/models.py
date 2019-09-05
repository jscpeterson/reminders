from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):

    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)

    def __str__(self):
        display_name = self.first_name + " " + self.last_name
        return display_name

    # @classmethod
    # def get_reverse_positions_dict(cls):
    #     """ Returns a dictionary where keys are strings of positions, and values are corresponding ints """
    #     return dict(((x[1], x[0]) for x in cls.POSITION_CHOICES))
    #
    # @classmethod
    # def get_positions_dict(cls):
    #     """ Returns a dictionary where keys are ints, and values are strings of positions """
    #     return dict(((x[0], x[1]) for x in cls.POSITION_CHOICES))

    # @classmethod
    # def get_position_disp(cls, position):
    #     """ Returns string representation of position given integer """
    #     positions_dict = cls.get_positions_dict()
    #     return positions_dict.get(position)


class Position(models.Model):

    role = models.CharField()
    users = models.ManyToManyField(CustomUser, related_name='position')
