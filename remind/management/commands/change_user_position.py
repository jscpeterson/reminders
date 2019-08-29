from django.core.management.base import BaseCommand
from users.models import CustomUser


class Command(BaseCommand):
    help = 'Changes a staff member\'s position, for example \'change_user_position "Joseph Peterson" "supervisor"\' '

    positions = {
            'supervisor': CustomUser.SUPERVISOR,
            'prosecutor': CustomUser.PROSECUTOR,
            'secretary': CustomUser.SECRETARY,
    }

    def add_arguments(self, parser):
        parser.add_argument('--user', type=str, required=True)
        parser.add_argument('--position', type=str, required=True)

    def handle(self, *args, **kwargs):
        first_name = kwargs['user'].split(' ')[0]
        last_name = kwargs['user'].split(' ')[1]
        position = kwargs['position'].lower()

        # Check user exists
        if not CustomUser.objects.filter(first_name=first_name, last_name=last_name).exists():
            raise Exception('{first_name} {last_name} not recognized as a user.'.format(
                first_name=first_name,
                last_name=last_name,
            ))

        # Check position is accurate
        if not position in self.positions.keys():
            raise Exception('{position} not recognized as a valid position.'.format(position=position))

        user = CustomUser.objects.get(first_name=first_name, last_name=last_name)
        user.position = self.positions[position]
        user.save()
        print('{user} is now a {position}.'.format(
                user=user,
                position=user.get_position_disp(user.position)
             ))

