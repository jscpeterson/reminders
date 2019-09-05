from django.core.management.base import BaseCommand
from users.models import CustomUser


class Command(BaseCommand):
    help = 'Removes supervisor privileges from a user.'

    def add_arguments(self, parser):
        parser.add_argument('--user', type=str, required=True)

    def handle(self, *args, **kwargs):
        first_name = kwargs['user'].split(' ')[0]
        last_name = kwargs['user'].split(' ')[1]

        # Check user exists
        if not CustomUser.objects.filter(first_name=first_name, last_name=last_name).exists():
            raise Exception('{first_name} {last_name} not recognized as a user.'.format(
                first_name=first_name,
                last_name=last_name,
            ))

        user = CustomUser.objects.get(first_name=first_name, last_name=last_name)

        if not user.is_supervisor:
            print('{} is not a supervisor.'.format(user))
        else:
            user.is_supervisor = False
            user.save(update_fields=['is_supervisor'])
            print('Supervisor privileges have been removed from {}.'.format(user))
