from django.core.management.base import BaseCommand
from remind.constants import DEADLINE_DESCRIPTIONS
from remind.models import Deadline


class Command(BaseCommand):
    help = 'Expires a single deadline based on its primary key.'

    def add_arguments(self, parser):
        parser.add_argument('--pk', type=int, required=True)

    def handle(self, *args, **kwargs):
        deadline = Deadline.objects.get(pk=kwargs['pk'])
        deadline.status = Deadline.EXPIRED
        deadline.save(update_fields=['status'])
        print('{deadline_desc} is EXPIRED.'.format(
            deadline_desc=DEADLINE_DESCRIPTIONS[str(deadline.type)].capitalize(),)
        )
