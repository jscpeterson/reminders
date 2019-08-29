from django.core.management.base import BaseCommand
from users.models import CustomUser


class Command(BaseCommand):
    help = 'Gets all users who have not been assigned positions.'

    def handle(self, *args, **kwargs):
        unassigned_users = CustomUser.objects.filter(position=None)
        print('The following {num} users do not have positions: '.format(
              num=len(unassigned_users)
        ))
        print(*unassigned_users, sep = ", ")

